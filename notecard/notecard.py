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
from .timeout import start_timeout, has_timed_out
from .transaction_manager import TransactionManager

use_periphery = False
use_serial_lock = False

if sys.implementation.name == 'cpython' and (sys.platform == 'linux' or sys.platform == 'linux2'):

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

# The notecard is a real-time device that has a fixed size interrupt buffer.
# We can push data at it far, far faster than it can process it,
# therefore we push it in segments with a pause between each segment.
CARD_REQUEST_SEGMENT_MAX_LEN = 250
# "a 250ms delay is required to separate "segments", ~256 byte
# I2C transactions." See
# https://dev.blues.io/guides-and-tutorials/notecard-guides/serial-over-i2c-protocol/#data-write
CARD_REQUEST_SEGMENT_DELAY_MS = 250
# "A 20ms delay is commonly used to separate smaller I2C transactions known as
# 'chunks'". See the same document linked above.
I2C_CHUNK_DELAY_MS = 20


def _prepare_request(req, debug=False):
    """Format the request string as a JSON object and add a newline."""
    req_json = json.dumps(req)
    if debug:
        print(req_json)

    req_json += "\n"
    return req_json


class NullContextManager:
    """A null context manager for use with NoOpSerialLock."""

    def __enter__(self):
        """Null enter function. Required for context managers."""
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """Null exit function. Required for context managers."""
        pass


class NoOpSerialLock():
    """A no-op serial lock class for when use_serial_lock is False."""

    def acquire(*args, **kwargs):
        """Acquire the no-op lock."""
        return NullContextManager()


def serial_lock(fn):
    """Attempt to get a lock on the serial channel used for Notecard comms."""

    def decorator(self, *args, **kwargs):
        try:
            with self.lock.acquire(timeout=5):
                return fn(self, *args, **kwargs)
        except SerialLockTimeout:
            raise Exception('Notecard in use')

    return decorator


class Notecard:
    """Base Notecard class.

    Primary Notecard Class, which provides a shared __init__
    to reset the Notecard via Serial or I2C.
    """

    def __init__(self):
        """Configure user agent."""
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
        self._transaction_manager = None

    def _preprocess_req(self, req):
        """Inspect the request for hub.set and add the User Agent."""
        if 'hub.set' in req.values():
            # Merge the User Agent to send along with the hub.set request.
            req = req.copy()
            req.update({'body': self.GetUserAgent()})

            self._user_agent_sent = True
        return req

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

    @serial_lock
    def _transmit(self, req):
        req = self._preprocess_req(req)
        req_json = _prepare_request(req, self._debug)

        try:
            transaction_timeout_secs = 30
            if self._transaction_manager:
                self._transaction_manager.start(transaction_timeout_secs)

            seg_off = 0
            seg_left = len(req_json)
            while seg_left > 0:
                seg_len = seg_left
                if seg_len > CARD_REQUEST_SEGMENT_MAX_LEN:
                    seg_len = CARD_REQUEST_SEGMENT_MAX_LEN

                self.uart.write(req_json[seg_off:seg_off + seg_len].encode('utf-8'))
                seg_off += seg_len
                seg_left -= seg_len
                time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)
        finally:
            if self._transaction_manager:
                self._transaction_manager.stop()

    @serial_lock
    def _transmit_and_receive(self, req):
        self._transmit(req)

        rsp_json = self.uart.readline()
        if self._debug:
            print(rsp_json.rstrip())

        return json.loads(rsp_json)

    def _read_byte_micropython(self):
        """Read a single byte from the Notecard (MicroPython)."""
        if not self.uart.any():
            return None
        return self.uart.read(1)

    def _read_byte_cpython(self):
        """Read a single byte from the Notecard (CPython)."""
        if self.uart.in_waiting == 0:
            return None
        return self.uart.read(1)

    def _read_byte_circuitpython(self):
        """Read a single byte from the Notecard (CircuitPython)."""
        return self.uart.read(1)

    def Command(self, req):
        """Send a command to the Notecard. The Notecard response is ignored."""
        if 'cmd' not in req:
            raise Exception("Please use 'cmd' instead of 'req'")

        self._transmit(req)

    def Transaction(self, req):
        """Perform a Notecard transaction and return the result."""
        return self._transmit_and_receive(req)

    @serial_lock
    def Reset(self):
        """Reset the Notecard."""
        for i in range(10):
            try:
                self.uart.write(b'\n')
            except:
                continue
            time.sleep(0.5)
            somethingFound = False
            nonControlCharFound = False
            while True:
                data = self._read_byte()
                if (data is None) or (data == b''):
                    break
                somethingFound = True
                if data[0] >= 0x20:
                    nonControlCharFound = True
            if somethingFound and not nonControlCharFound:
                break
            else:
                raise Exception('Notecard not responding')

    def __init__(self, uart_id, debug=False):
        """Initialize the Notecard before a reset."""
        super().__init__()
        self._user_agent['req_interface'] = 'serial'
        self._user_agent['req_port'] = str(uart_id)

        self.uart = uart_id
        self._debug = debug

        if use_serial_lock:
            self.lock = FileLock('serial.lock')
        else:
            self.lock = NoOpSerialLock()

        if sys.implementation.name == 'micropython':
            self._read_byte = self._read_byte_micropython
        elif sys.implementation.name == 'cpython':
            self._read_byte = self._read_byte_cpython
        elif sys.implementation.name == 'circuitpython':
            self._read_byte = self._read_byte_circuitpython
        else:
            raise NotImplementedError(f'Unsupported platform: {sys.implementation.name}')

        self.Reset()


class OpenI2C(Notecard):
    """Notecard class for I2C communication."""

    def _send_payload(self, json):
        chunk_offset = 0
        json_left = len(json)
        sent_in_seg = 0
        write_length = bytearray(1)

        while json_left > 0:
            chunk_len = min(json_left, self.max)
            write_length[0] = chunk_len
            write_data = bytes(json[chunk_offset:chunk_offset + chunk_len],
                               'utf-8')
            # Send a message with the length of the incoming bytes followed
            # by the bytes themselves.
            if use_periphery:
                msgs = [I2C.Message(write_length + write_data)]
                self.i2c.transfer(self.addr, msgs)
            else:
                self.i2c.writeto(self.addr, write_length + write_data)

            chunk_offset += chunk_len
            json_left -= chunk_len
            sent_in_seg += chunk_len

            if sent_in_seg > CARD_REQUEST_SEGMENT_MAX_LEN:
                sent_in_seg -= CARD_REQUEST_SEGMENT_MAX_LEN
                time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

            time.sleep(I2C_CHUNK_DELAY_MS / 1000)

    def _receive(self, timeout_secs, chunk_delay_secs, wait_for_newline):
        chunk_len = 0
        received_newline = False
        start = start_timeout()
        read_data = bytearray()

        while True:
            initiate_read = bytearray(2)
            # 0 indicates we are reading from the Notecard.
            initiate_read[0] = 0
            # This indicates how many bytes we are prepared to read.
            initiate_read[1] = chunk_len
            # read_buf is a buffer to store the data we're reading.
            # chunk_len accounts for the payload and the +2 is for the
            # header. The header sent by the Notecard has one byte to
            # indicate the number of bytes still available to read and a
            # second byte to indicate the number of bytes coming in the
            # current chunk.
            read_buf = bytearray(chunk_len + 2)

            if use_periphery:
                msgs = [I2C.Message(initiate_read), I2C.Message(read_buf, read=True)]
                self.i2c.transfer(self.addr, msgs)
                read_buf = msgs[1].data
            elif sys.implementation.name == 'micropython':
                self.i2c.writeto(self.addr, initiate_read, False)
                self.i2c.readfrom_into(self.addr, read_buf)
            else:
                self.i2c.writeto_then_readfrom(self.addr, initiate_read, read_buf)

            # The number of bytes still available to read.
            num_bytes_available = read_buf[0]
            # The number of bytes in this chunk.
            num_bytes_this_chunk = read_buf[1]
            if num_bytes_this_chunk > 0:
                read_data += read_buf[2:2 + num_bytes_this_chunk]
                received_newline = read_buf[-1] == ord('\n')

            chunk_len = min(num_bytes_available, self.max)
            # Keep going if there's still byte available to read, even if
            # we've received a newline.
            if chunk_len > 0:
                continue

            # Otherwise, if there's no bytes available to read and we either
            # 1) don't care about waiting for a newline or 2) do care and
            # received the newline, we're done.
            if not wait_for_newline or received_newline:
                break

            # Delay between reading chunks. Note that as long as bytes are
            # available to read (i.e. chunk_len > 0), we don't delay here, nor
            # do we check the timeout below. This is intentional and mimics the
            # behavior of other SDKs (e.g. note-c).
            time.sleep(chunk_delay_secs)

            if (timeout_secs != 0 and has_timed_out(start, timeout_secs)):
                raise Exception("Timed out while reading data from the Notecard.")

        return read_data

    def Command(self, req):
        """Perform a Notecard command and return with no response."""
        if 'cmd' not in req:
            raise Exception("Please use 'cmd' instead of 'req'")

        req = self._preprocess_req(req)
        req_json = _prepare_request(req, self._debug)

        while not self.lock():
            pass

        try:
            transaction_timeout_secs = 30
            if self._transaction_manager:
                self._transaction_manager.start(transaction_timeout_secs)

            self._send_payload(req_json)
        finally:
            self.unlock()
            if self._transaction_manager:
                self._transaction_manager.stop()

    def Transaction(self, req):
        """Perform a Notecard transaction and return the result."""
        req = self._preprocess_req(req)
        req_json = _prepare_request(req, self._debug)
        rsp_json = ""

        while not self.lock():
            pass

        try:
            transaction_timeout_secs = 30
            if self._transaction_manager:
                self._transaction_manager.start(transaction_timeout_secs)

            self._send_payload(req_json)

            read_data = self._receive(transaction_timeout_secs, 0.05, True)
            rsp_json = "".join(map(chr, read_data))
        finally:
            self.unlock()
            if self._transaction_manager:
                self._transaction_manager.stop()

        if self._debug:
            print(rsp_json.rstrip())

        return json.loads(rsp_json)

    def Reset(self):
        """Reset the Notecard."""
        while not self.lock():
            pass

        try:
            # Read from the Notecard until there's nothing left to read.
            self._receive(0, .001, False)
        finally:
            self.unlock()

    def lock(self):
        """Lock the I2C port so the host can interact with the Notecard."""
        if use_i2c_lock:
            return self.i2c.try_lock()
        return True

    def unlock(self):
        """Unlock the I2C port."""
        if use_i2c_lock:
            return self.i2c.unlock()
        return True

    def __init__(self, i2c, address, max_transfer, debug=False):
        """Initialize the Notecard before a reset."""
        super().__init__()
        self._user_agent['req_interface'] = 'i2c'
        self._user_agent['req_port'] = address

        self.i2c = i2c
        self._debug = debug
        if address == 0:
            self.addr = NOTECARD_I2C_ADDRESS
        else:
            self.addr = address
        if max_transfer == 0:
            self.max = 255
        else:
            self.max = max_transfer

        self.Reset()
