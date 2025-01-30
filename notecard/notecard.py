"""Main module for note-python."""

##
# @mainpage Python Library for the Notecard
#
# @section intro_sec Introduction
# This module contains the core functionality for running the
# note-python library, including the main Notecard class, and
# Serial and I2C sub-classes.
#
# @section dependencies Dependencies
#
# This library requires a physical connection to a Notecard over I2C or
# Serial to be functional.
# @section author Author
#
# Written by Ray Ozzie and Brandon Satrom for Blues Inc.
# @section license License
#
# Copyright (c) 2019 Blues Inc. MIT License. Use of this source code is
# governed by licenses granted by the copyright holder including that found in
# the
# <a href="https://github.com/blues/note-python/blob/master/LICENSE">
#   LICENSE
# </a>
# file.

##
# @file notecard.py
#
# @brief Main module for note-python. Contains core library functionality.

import sys
import os
import json
import time
from notecard.timeout import start_timeout, has_timed_out
from notecard.transaction_manager import TransactionManager, NoOpTransactionManager
from notecard.crc32 import crc32

use_periphery = False
use_serial_lock = False

if sys.implementation.name == 'cpython' and (sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin'):
    use_periphery = True
    from periphery import I2C

    use_serial_lock = True
    from filelock import FileLock
    from filelock import Timeout as SerialLockTimeout
else:
    class SerialLockTimeout(Exception):
        """A null SerialLockTimeout for when use_serial_lock is False."""

        pass

use_i2c_lock = not use_periphery and sys.implementation.name != 'micropython'

NOTECARD_I2C_ADDRESS = 0x17
NOTECARD_I2C_MAX_TRANSFER_DEFAULT = 255

# The notecard is a real-time device that has a fixed size interrupt buffer. We
# can push data at it far, far faster than it can process it. Therefore, we push
# it in segments with a pause between each segment.
CARD_REQUEST_SEGMENT_MAX_LEN = 250
# "a 250ms delay is required to separate "segments", ~256 byte I2C
# transactions." See
# https://dev.blues.io/guides-and-tutorials/notecard-guides/serial-over-i2c-protocol/#data-write
CARD_REQUEST_SEGMENT_DELAY_MS = 250
# "A 20ms delay is commonly used to separate smaller I2C transactions known as
# 'chunks'". See the same document linked above.
CARD_REQUEST_I2C_CHUNK_DELAY_MS = 20
# The delay, in miliseconds, to wait after receiving a NACK I2C.
CARD_REQUEST_I2C_NACK_WAIT_MS = 1000
# The number of times to retry syncing up with the Notecard during a reset
# before giving up.
CARD_RESET_SYNC_RETRIES = 10
# The time, in miliseconds, to drain incoming messages during a reset.
CARD_RESET_DRAIN_MS = 500
CARD_INTER_TRANSACTION_TIMEOUT_SEC = 30
CARD_INTRA_TRANSACTION_TIMEOUT_SEC = 1
CARD_TRANSACTION_RETRIES = 5


class NoOpContextManager:
    """A no-op context manager for use with NoOpSerialLock."""

    def __enter__(self):
        """No-op enter function. Required for context managers."""
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """No-op exit function. Required for context managers."""
        pass


class NoOpSerialLock():
    """A no-op serial lock class for when use_serial_lock is False."""

    def acquire(*args, **kwargs):
        """Acquire the no-op lock."""
        return NoOpContextManager()

    def release(*args, **kwargs):
        """Release the no-op lock."""
        pass


class Notecard:
    """Base Notecard class."""

    def __init__(self, debug=False):
        """Initialize the Notecard object."""
        self._user_agent_app = None
        self._user_agent_sent = False
        self._user_agent = {
            'agent': 'note-python',
            'os_name': sys.implementation.name,
            'os_platform': sys.platform,
            'os_version': sys.version
        }
        if sys.implementation.name == 'cpython':
            self._user_agent['os_family'] = os.name
        else:
            self._user_agent['os_family'] = os.uname().machine
        self._transaction_manager = NoOpTransactionManager()
        self._debug = debug
        self._last_request_seq_number = 0
        self._card_supports_crc = False
        self._reset_required = True

    def _crc_add(self, req_string, seq_number):
        """Add a CRC field to the request.

        The CRC field also contains a sequence number and has this format:

            "crc":"SSSS:CCCCCCCC"

        SSSS is the sequence number encoded as a string of 4 hex digits.
        CCCCCCCC is the CRC32 encoded as a string of 8 hex digits.
        """
        req_bytes = req_string.encode('utf-8')
        crc_hex = '{:08x}'.format(crc32(req_bytes))
        seq_number_hex = '{:04x}'.format(seq_number)
        crc_field = f'"crc":"{seq_number_hex}:{crc_hex}"'
        req_string_w_crc = req_string[:-1]
        if req_string[-2] == '{':
            req_string_w_crc += f'{crc_field}'
        else:
            req_string_w_crc += f',{crc_field}'
        req_string_w_crc += '}'

        return req_string_w_crc

    def _crc_error(self, rsp_bytes):
        """Check the CRC in a Notecard response."""
        rsp_json = json.loads(rsp_bytes)
        if 'crc' not in rsp_json:
            # If there's not a 'crc' field in the response, it's only an error
            # if the Notecard supports CRC.
            return self._card_supports_crc

        self._card_supports_crc = True

        # Extract the sequence number and CRC. We do all this via string
        # operations instead of decoding the JSON. In Python, numbers with long
        # decimal parts (e.g. 10.11111111111111123445522123) get truncated in
        # the decoding process. When re-encoded, the string representation is
        # also truncated, and so the CRC will be computed over a different
        # string than was originally sent, resulting in a CRC error.
        seq_number, crc = rsp_json['crc'].split(':')

        # Convert the received CRC and sequence number to integers for later
        # comparison.
        try:
            seq_number_as_int = int(seq_number, 16)
        except ValueError:
            if self._debug:
                print(f'Received sequence number "{seq_number}" cannot be ' + \
                      'converted to integer.')
            return True
        try:
            crc_as_int = int(crc, 16)
        except ValueError:
            if self._debug:
                print(f'Received CRC "{crc}" cannot be converted to integer.')
            return True

        # Remove the 'crc' field from the response.
        rsp_str = rsp_bytes.decode()
        rsp_str_crc_removed = rsp_str.split('"crc":')[0]
        if rsp_str_crc_removed[-1] == ',':
            rsp_str_crc_removed = rsp_str_crc_removed[:-1] + '}'
        else:
            rsp_str_crc_removed = rsp_str_crc_removed.rstrip() + '}'

        # Compute the CRC over the response, with the 'crc' field removed.
        bytes_for_crc_calc = rsp_str_crc_removed.encode('utf-8')
        computed_crc = crc32(bytes_for_crc_calc)

        if seq_number_as_int != self._last_request_seq_number:
            if self._debug:
                print('Sequence number mismatch. Expected ' + \
                      f'{self._last_request_seq_number}, received ' + \
                      f'{seq_number_as_int}.')
            return True
        elif crc_as_int != computed_crc:
            if self._debug:
                print(f'CRC error. Computed {computed_crc}, received ' + \
                      f'{crc_as_int}.')
            return True

        return False

    def _prepare_request(self, req):
        """Prepare a request for transmission to the Notecard."""
        # Inspect the request for hub.set and add the User Agent.
        if 'hub.set' in req.values():
            # Merge the User Agent to send along with the hub.set request.
            req = req.copy()
            req.update({'body': self.GetUserAgent()})

            self._user_agent_sent = True

        rsp_expected = 'req' in req

        # If this is a request and not a command, add a CRC.
        req_string = json.dumps(req, separators=(',', ':'))
        if rsp_expected:
            req_string = self._crc_add(req_string,
                                       self._last_request_seq_number)

        # Serialize the JSON request to a string, removing any unnecessary
        # whitespace.
        if self._debug:
            print(req_string)

        req_string += "\n"

        # Encode the request string as UTF-8 bytes.
        return (req_string.encode('utf-8'), rsp_expected)

    def _transaction_timeout_seconds(self, req):
        """Determine the timeout to use, in seconds, for the transaction.

        When note.add or web.* requests are used to transfer binary data, the
        time to complete the transaction varies depending on the size of the
        payload and network conditions. Therefore, it's possible for these
        transactions to timeout prematurely.

        This method does the following:
          - If the request is a `note.add`, set the timeout value to the
            value of the "milliseconds" parameter, if it exists. If it
            doesn't, use the "seconds" parameter. If that doesn't exist,
            use the standard timeout of `CARD_INTER_TRANSACTION_TIMEOUT_SEC`.
          - If the request is a `web.*`, follow the same logic, but instead
            of using the standard timeout, use 90 seconds for all `web.*`
            transactions.
        """
        timeout_secs = CARD_INTER_TRANSACTION_TIMEOUT_SEC
        if 'req' in req:
            req_key = 'req'
        elif 'cmd' in req:
            req_key = 'cmd'
        else:
            raise Exception('Malformed request. Missing \'req\' or \'cmd\' ' + \
                            f'field: {req}.')

        if req[req_key] == 'note.add':
            if 'milliseconds' in req:
                timeout_secs = req['milliseconds'] / 1000
            elif 'seconds' in req:
                timeout_secs = req['seconds']
        elif 'web.' in req[req_key]:
            if 'milliseconds' in req:
                timeout_secs = req['milliseconds'] / 1000
            elif 'seconds' in req:
                timeout_secs = req['seconds']
            else:
                timeout_secs = 90

        if self._debug:
            print(f'Using transaction timeout of {timeout_secs} seconds.')

        return timeout_secs

    def Transaction(self, req, lock=True):
        """Send a request to the Notecard and read back a response.

        If the request is a command (indicated by using 'cmd' in the request
        instead of 'req'), don't return a response.

        The underlying transport channel (serial or I2C) is locked for the
        duration of the request and response if `lock` is True.
        """
        rsp_json = None
        timeout_secs = self._transaction_timeout_seconds(req)
        req_bytes, rsp_expected = self._prepare_request(req)

        if self._reset_required:
            self.Reset()

        try:
            self._transaction_manager.start(CARD_INTER_TRANSACTION_TIMEOUT_SEC)
            if lock:
                self.lock()

            retries_left = CARD_TRANSACTION_RETRIES
            error = False
            if rsp_expected:
                while retries_left > 0:
                    try:
                        rsp_bytes = self._transact(
                            req_bytes, rsp_expected=True,
                            timeout_secs=timeout_secs)
                    except Exception as e:
                        if self._debug:
                            print(e)

                        error = True
                        self.Reset()
                        retries_left -= 1
                        time.sleep(0.5)
                        continue

                    if self._crc_error(rsp_bytes):
                        if self._debug:
                            print('CRC error on response from Notecard.')

                        error = True
                        retries_left -= 1
                        time.sleep(0.5)
                        continue

                    try:
                        rsp_json = json.loads(rsp_bytes)
                    except Exception as e:
                        if self._debug:
                            print(e)

                        error = True
                        retries_left -= 1
                        time.sleep(0.5)
                        continue

                    if 'err' in rsp_json:
                        if '{io}' in rsp_json['err'] and '{not-supported}' not in rsp_json['err']:
                            if self._debug:
                                print('Response has error field indicating ' + \
                                      f'I/O error: {rsp_json}')

                            error = True
                            retries_left -= 1
                            time.sleep(0.5)
                            continue
                        elif '{bad-bin}' in rsp_json['err']:
                            if self._debug:
                                print('Response has error field indicating ' + \
                                      f'binary I/O error: {rsp_json}')
                                print('Not eligible for retry.')

                            error = True
                            break

                    error = False
                    break
            else:
                try:
                    self._transact(req_bytes, rsp_expected=False,
                                   timeout_secs=timeout_secs)
                except Exception as e:
                    error = True
                    if self._debug:
                        print(e)

            self._last_request_seq_number += 1

            if error:
                self._reset_required = True
                raise Exception('Failed to transact with Notecard.')

        finally:
            if lock:
                self.unlock()

            self._transaction_manager.stop()

        if self._debug and rsp_json is not None:
            print(rsp_json)

        return rsp_json

    def Command(self, req):
        """Send a command to the Notecard.

        Unlike `Transaction`, `Command` doesn't return a response from the
        Notecard.
        """
        if 'cmd' not in req:
            raise Exception("Please use 'cmd' instead of 'req'")

        self.Transaction(req)

    def GetUserAgent(self):
        """Return the User Agent String for the host for debug purposes."""
        ua_copy = self._user_agent.copy()
        ua_copy.update(self._user_agent_app or {})
        return ua_copy

    def SetAppUserAgent(self, app_user_agent):
        """Set the User Agent info for the app."""
        self._user_agent_app = app_user_agent

    def UserAgentSent(self):
        """Return true if the User Agent has been sent to the Notecard."""
        return self._user_agent_sent

    def SetTransactionPins(self, rtx_pin, ctx_pin):
        """Set the pins used for RTX and CTX."""
        self._transaction_manager = TransactionManager(rtx_pin, ctx_pin)


class OpenSerial(Notecard):
    """Notecard class for Serial communication."""

    def _transact(self, req_bytes, rsp_expected,
                  timeout_secs=CARD_INTER_TRANSACTION_TIMEOUT_SEC):
        self.transmit(req_bytes)

        if not rsp_expected:
            return

        start = start_timeout()
        while not self._available():
            if timeout_secs != 0 and has_timed_out(start, timeout_secs):
                raise Exception('Timed out while querying Notecard for ' + \
                                'available data.')

            # Delay for 10 ms before checking for available data again.
            time.sleep(.01)

        return self.receive()

    def receive(self, timeout_secs=CARD_INTRA_TRANSACTION_TIMEOUT_SEC,
                delay=True):
        """Read a newline-terminated batch of data from the Notecard."""
        data = bytearray()
        received_newline = False
        start = start_timeout()

        while not received_newline:
            while not self._available():
                if timeout_secs != 0 and has_timed_out(start, timeout_secs):
                    raise Exception('Timed out waiting to receive data from' + \
                                    ' Notecard.')

                # Sleep while awaiting the first byte (lazy). After the first
                # byte, start to spin for the remaining bytes (greedy).
                if delay and len(data) == 0:
                    time.sleep(.001)

            timeout_secs = CARD_INTRA_TRANSACTION_TIMEOUT_SEC
            start = start_timeout()
            byte = self._read_byte()
            data.extend(byte)
            received_newline = byte == b'\n'

        return data

    def transmit(self, data, delay=True):
        """Send `data` to the Notecard."""
        seg_off = 0
        seg_left = len(data)

        while seg_left > 0:
            seg_len = seg_left
            if seg_len > CARD_REQUEST_SEGMENT_MAX_LEN:
                seg_len = CARD_REQUEST_SEGMENT_MAX_LEN

            self.uart.write(data[seg_off:seg_off + seg_len])
            seg_off += seg_len
            seg_left -= seg_len

            if delay:
                time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

    def _available_micropython(self):
        return self.uart.any()

    def _available_default(self):
        return self.uart.in_waiting > 0

    def _read_byte(self):
        """Read a single byte from the Notecard."""
        return self.uart.read(1)

    def Reset(self):
        """Reset the Notecard."""
        if self._debug:
            print('Resetting Notecard serial communications.')

        # Delay to give the Notecard a chance to process any segment sent prior
        # to the coming reset sequence.
        time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

        notecard_ready = False
        try:
            self.lock()

            for i in range(CARD_RESET_SYNC_RETRIES):
                try:
                    # Send a newline to the Notecard to terminate any partial
                    # request that might be sitting in its input buffer.
                    self.uart.write(b'\n')
                except Exception as e:
                    if self._debug:
                        print(e)
                    # Wait CARD_RESET_DRAIN_MS and before trying to send the
                    # newline again.
                    time.sleep(CARD_RESET_DRAIN_MS / 1000)
                    continue

                something_found = False
                non_control_char_found = False
                # Drain serial for 500 ms.
                start = start_timeout()
                while not has_timed_out(start, CARD_RESET_DRAIN_MS / 1000):
                    while self._available():
                        something_found = True
                        data = self._read_byte()
                        if data[0] != ord('\n') and data[0] != ord('\r'):
                            non_control_char_found = True
                            # Reset the timer with each non-control character.
                            start = start_timeout()

                    # If there was no data read from the Notecard, wait 1 ms and
                    # try again. Keep doing this for CARD_RESET_DRAIN_MS.
                    time.sleep(.001)

                if not something_found:
                    if self._debug:
                        print('Notecard not responding to newline during ' + \
                              'reset.')

                elif non_control_char_found:
                    if self._debug:
                        print('Received non-control characters from the ' + \
                              'Notecard during reset.')
                else:
                    # If all we got back is newlines, we're in sync with the
                    # Notecard.
                    notecard_ready = True
                    break

                if self._debug:
                    print('Retrying reset...')

                # Wait CARD_RESET_DRAIN_MS before trying again.
                time.sleep(CARD_RESET_DRAIN_MS / 1000)

            if not notecard_ready:
                raise Exception('Failed to reset Notecard.')

        finally:
            self.unlock()

        self._reset_required = False

    def lock(self):
        """Lock access to the serial bus."""
        self.lock_handle.acquire(timeout=5)

    def unlock(self):
        """Unlock access to the serial bus."""
        self.lock_handle.release()

    def __init__(self, uart_id, debug=False, lock_path=None):
        """Initialize the Notecard before a reset.

        Args:
            uart_id: The serial port identifier.
            debug: Enable debug output if True.
            lock_path: Optional path for the serial lock file. Defaults to /tmp/serial.lock
                or the value of NOTECARD_SERIAL_LOCK_PATH environment variable.
        """
        super().__init__(debug)
        self._user_agent['req_interface'] = 'serial'
        self._user_agent['req_port'] = str(uart_id)

        self.uart = uart_id

        if use_serial_lock:
            if lock_path is None:
                lock_path = os.environ.get('NOTECARD_SERIAL_LOCK_PATH', '/tmp/serial.lock')
            self.lock_handle = FileLock(lock_path)
        else:
            self.lock_handle = NoOpSerialLock()

        if sys.implementation.name == 'micropython':
            self._available = self._available_micropython
        else:
            if hasattr(self.uart, 'in_waiting'):
                self._available = self._available_default
            else:
                raise NotImplementedError('Serial communications with the ' + \
                                          'Notecard are not supported for ' + \
                                          'this platform.')

        self.Reset()


class OpenI2C(Notecard):
    """Notecard class for I2C communication."""

    def _read(self, length):
        """Perform a serial-over-I2C read."""
        initiate_read = bytearray(2)
        # 0 indicates we are reading from the Notecard.
        initiate_read[0] = 0
        # This indicates how many bytes we are prepared to read.
        initiate_read[1] = length
        # read_buf is a buffer to store the data we're reading.
        # length accounts for the payload and the +2 is for the header. The
        # header sent by the Notecard has one byte to indicate the number of
        # bytes still available to read and a second byte to indicate the number
        # of bytes coming in the current packet.
        read_buf = bytearray(length + 2)

        self._platform_read(initiate_read, read_buf)
        # First two bytes are the header.
        header = read_buf[0:2]
        # The number of bytes still available to read after this packet.
        available = header[0]
        # The number of data bytes in this packet.
        data_len = header[1]
        # The rest is the data.
        data = read_buf[2:]

        if len(data) != data_len:
            raise Exception('Serial-over-I2C error: reported data length ' + \
                            f'({data_len}) differs from actual data length' + \
                            f' ({len(data)}).')

        return available, data

    def _write(self, data):
        """Perform a serial-over-I2C write."""
        self._platform_write(bytearray([len(data)]), data)

    def receive(self, timeout_secs=CARD_INTRA_TRANSACTION_TIMEOUT_SEC,
                delay=True):
        """Read a newline-terminated batch of data from the Notecard."""
        read_len = 0
        received_newline = False
        timeout_secs = CARD_INTER_TRANSACTION_TIMEOUT_SEC
        start = start_timeout()
        received_data = bytearray()

        while True:
            available, data = self._read(read_len)
            if len(data) > 0:
                received_data += data

                timeout_secs = CARD_INTRA_TRANSACTION_TIMEOUT_SEC
                start = start_timeout()

                if not received_newline:
                    received_newline = data[-1] == ord('\n')

            read_len = min(available, self.max)
            # Keep going if there are still bytes available to read, even if
            # we've received a newline.
            if available > 0:
                continue

            # Otherwise, if there are no bytes available to read and we either
            # 1) don't care about waiting for a newline or 2) do care and
            # received the newline, we're done.
            if received_newline:
                break

            if timeout_secs != 0 and has_timed_out(start, timeout_secs):
                raise Exception('Timed out while reading data from the ' + \
                                'Notecard.')

            if delay:
                time.sleep(0.05)

        return received_data

    def transmit(self, data, delay=True):
        """Send `data` to the Notecard."""
        chunk_offset = 0
        data_left = len(data)
        sent_in_seg = 0

        while data_left > 0:
            # Delay for 5ms. This prevents a fast host from hammering a
            # slow/busy Notecard with requests.
            time.sleep(.005)

            chunk_len = min(data_left, self.max)
            write_data = data[chunk_offset:chunk_offset + chunk_len]
            self._write(write_data)

            chunk_offset += chunk_len
            data_left -= chunk_len
            sent_in_seg += chunk_len

            # We delay for CARD_REQUEST_SEGMENT_DELAY_MS ms every time a full
            # "segment" of data has been transmitted.
            if sent_in_seg > CARD_REQUEST_SEGMENT_MAX_LEN:
                sent_in_seg -= CARD_REQUEST_SEGMENT_MAX_LEN

                if delay:
                    time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

            if delay:
                time.sleep(CARD_REQUEST_I2C_CHUNK_DELAY_MS / 1000)

    def _transact(self, req_bytes, rsp_expected,
                  timeout_secs=CARD_INTER_TRANSACTION_TIMEOUT_SEC):
        self.transmit(req_bytes)

        if not rsp_expected:
            return

        # Delay for 5ms. This prevents a fast host from hammering a slow/busy
        # Notecard with requests.
        time.sleep(0.005)

        # Query the Notecard every 50 ms to see if there's data available to
        # read.
        start = start_timeout()
        available = 0
        while available == 0:
            available, _ = self._read(0)

            if timeout_secs != 0 and has_timed_out(start, timeout_secs):
                raise Exception('Timed out while querying Notecard for ' + \
                                'available data.')

            time.sleep(0.05)

        return self.receive()

    def Reset(self):
        """Reset the Notecard."""
        if self._debug:
            print('Resetting Notecard I2C communications.')

        notecard_ready = False
        try:
            self.lock()

            for i in range(CARD_RESET_SYNC_RETRIES):
                try:
                    # Send a newline to the Notecard to terminate any partial
                    # request that might be sitting in its input buffer.
                    self._write(b'\n')
                except Exception as e:
                    if self._debug:
                        print(e)
                    time.sleep(CARD_REQUEST_I2C_NACK_WAIT_MS / 1000)
                    continue

                time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

                something_found = False
                non_control_char_found = False

                start = start_timeout()
                read_len = 0
                while not has_timed_out(start, CARD_RESET_DRAIN_MS / 1000):
                    try:
                        available, data = self._read(read_len)
                    except Exception as e:
                        if self._debug:
                            print(e)
                        time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)
                        continue

                    if len(data) > 0:
                        something_found = True
                        # The Notecard responds to a bare `\n` with `\r\n`. If
                        # we get any other characters back, it means the host
                        # and Notecard aren't synced up yet, and we need to
                        # transmit `\n` again.
                        for byte in data:
                            if byte != ord('\n') and byte != ord('\r'):
                                non_control_char_found = True
                                # Reset the timer with each non-control
                                # character.
                                start = start_timeout()

                    read_len = min(available, self.max)

                    time.sleep(CARD_REQUEST_I2C_CHUNK_DELAY_MS / 1000)

                if not something_found:
                    if self._debug:
                        print('Notecard not responding to newline during ' + \
                              'reset.')
                    time.sleep(.005)
                elif non_control_char_found:
                    if self._debug:
                        print('Received non-control characters from the ' + \
                              'Notecard during reset.')
                else:
                    # If all we got back is newlines, we're in sync with the
                    # Notecard.
                    notecard_ready = True
                    break

                if self._debug:
                    print('Retrying reset...')

                # Wait CARD_RESET_DRAIN_MS before trying again.
                time.sleep(CARD_RESET_DRAIN_MS / 1000)
        finally:
            self.unlock()

        if not notecard_ready:
            raise Exception('Failed to reset Notecard.')

        self._reset_required = False

    def _cpython_write(self, length, data):  # noqa: D403
        """CPython implementation of serial-over-I2C write."""
        msgs = [I2C.Message(length + data)]
        self.i2c.transfer(self.addr, msgs)

    def _non_cpython_write(self, length, data):
        """Non-CPython implementation of serial-over-I2C write."""
        self.i2c.writeto(self.addr, length + data)

    def _cpython_read(self, initiate_read_msg, read_buf):  # noqa: D403
        """CPython implementation of serial-over-I2C read."""
        msgs = [
            I2C.Message(initiate_read_msg),
            I2C.Message(read_buf, read=True)
        ]
        self.i2c.transfer(self.addr, msgs)
        read_bytes = msgs[1].data
        read_buf[:len(read_bytes)] = read_bytes

    def _micropython_read(self, initiate_read_msg, read_buf):  # noqa: D403
        """MicroPython implementation of serial-over-I2C read."""
        self.i2c.writeto(self.addr, initiate_read_msg, False)
        self.i2c.readfrom_into(self.addr, read_buf)

    def _circuitpython_read(self, initiate_read_msg, read_buf):  # noqa: D403
        """CircuitPython implementation of serial-over-I2C read."""
        self.i2c.writeto_then_readfrom(self.addr, initiate_read_msg, read_buf)

    def lock(self):
        """Lock access to the I2C bus."""
        retries = 5
        while retries != 0:
            if self.lock_fn():
                break

            retries -= 1
            # Try again after 100 ms.
            time.sleep(.1)

        if retries == 0:
            raise Exception('Failed to acquire I2C lock.')

    def unlock(self):
        """Unlock access to the I2C bus."""
        self.unlock_fn()

    def _i2c_no_op_try_lock(*args, **kwargs):
        """No-op lock function."""
        return True

    def _i2c_no_op_unlock(*args, **kwargs):
        """No-op unlock function."""
        pass

    def __init__(self, i2c, address, max_transfer, debug=False):
        """Initialize the Notecard before a reset."""
        super().__init__(debug)
        self._user_agent['req_interface'] = 'i2c'
        self._user_agent['req_port'] = address

        self.i2c = i2c

        if use_i2c_lock:
            self.lock_fn = self.i2c.try_lock
            self.unlock_fn = self.i2c.unlock
        else:
            self.lock_fn = self._i2c_no_op_try_lock
            self.unlock_fn = self._i2c_no_op_unlock

        if address == 0:
            self.addr = NOTECARD_I2C_ADDRESS
        else:
            self.addr = address
        if max_transfer == 0:
            self.max = NOTECARD_I2C_MAX_TRANSFER_DEFAULT
        else:
            self.max = max_transfer

        if sys.implementation.name == 'micropython':
            self._platform_write = self._non_cpython_write
            self._platform_read = self._micropython_read
        elif sys.implementation.name == 'circuitpython':
            self._platform_write = self._non_cpython_write
            self._platform_read = self._circuitpython_read
        else:
            self._platform_write = self._cpython_write
            self._platform_read = self._cpython_read

        self.Reset()
