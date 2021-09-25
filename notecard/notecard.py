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

use_periphery = False
use_micropython = False
use_serial_lock = False
use_circuitpython = sys.implementation.name == 'circuitpython'
use_micropython = sys.implementation.name == 'micropython'
use_rtc = not use_micropython and not use_circuitpython

if sys.implementation.name == 'cpython':
    if sys.platform == 'linux' or sys.platform == 'linux2':
        use_periphery = True
        from periphery import I2C

        use_serial_lock = True
        from filelock import Timeout, FileLock

use_i2c_lock = not use_periphery and not use_micropython


NOTECARD_I2C_ADDRESS = 0x17

# The notecard is a real-time device that has a fixed size interrupt buffer.
# We can push data at it far, far faster than it can process it,
# therefore we push it in segments with a pause between each segment.
CARD_REQUEST_SEGMENT_MAX_LEN = 250
CARD_REQUEST_SEGMENT_DELAY_MS = 250

if not use_rtc:
    if use_circuitpython:
        import supervisor
        from supervisor import ticks_ms

        def ticks_diff(ticks1, ticks2):
            """Compute the signed difference between two ticks values."""
            diff = (ticks1 - ticks2) & _TICKS_MAX  # noqa: F821
            diff = ((diff + _TICKS_HALFPERIOD)  # noqa: F821
                    & _TICKS_MAX) - _TICKS_HALFPERIOD  # noqa: F821
            return diff
    if use_micropython:
        from utime import ticks_diff, ticks_ms  # noqa: F811


def has_timed_out(start, timeout_secs):
    """Determine whether a timeout interval has passed during communication."""
    if not use_rtc:
        return ticks_diff(ticks_ms(), start) > timeout_secs * 1000
    else:
        return time.time() > start + timeout_secs


def start_timeout():
    """Start the timeout interval for I2C communication."""
    return ticks_ms() if not use_rtc else time.time()


def prepareRequest(req, debug=False):
    """Format the request string as a JSON object and add a newline."""
    req_json = json.dumps(req)
    if debug:
        print(req_json)

    req_json += "\n"
    return req_json


def serialReadByte(port):
    """Read a single byte from a Notecard."""
    if sys.implementation.name == 'micropython':
        if not port.any():
            return None
    elif sys.implementation.name == 'cpython':
        if port.in_waiting == 0:
            return None
    return port.read(1)


def serialReset(port):
    """Send a reset command to a Notecard."""
    for i in range(10):
        try:
            port.write(b'\n')
        except:
            continue
        time.sleep(0.5)
        somethingFound = False
        nonControlCharFound = False
        while True:
            data = serialReadByte(port)
            if (data is None) or (data == b''):
                break
            somethingFound = True
            if data[0] >= 0x20:
                nonControlCharFound = True
        if somethingFound and not nonControlCharFound:
            break
        else:
            raise Exception("Notecard not responding")


def serialTransaction(port, req, debug):
    """Perform a single write to and read from a Notecard."""
    req_json = prepareRequest(req, debug)

    seg_off = 0
    seg_left = len(req_json)
    while True:
        seg_len = seg_left
        if seg_len > CARD_REQUEST_SEGMENT_MAX_LEN:
            seg_len = CARD_REQUEST_SEGMENT_MAX_LEN

        port.write(req_json[seg_off:seg_off + seg_len]
                   .encode('utf-8'))
        seg_off += seg_len
        seg_left -= seg_len
        if seg_left == 0:
            break
        time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

    rsp_json = port.readline()

    if debug:
        print(rsp_json.rstrip())

    rsp = json.loads(rsp_json)
    return rsp


def serialCommand(port, req, debug):
    """Perform a single write to and read from a Notecard."""
    req_json = prepareRequest(req, debug)

    seg_off = 0
    seg_left = len(req_json)
    while True:
        seg_len = seg_left
        if seg_len > CARD_REQUEST_SEGMENT_MAX_LEN:
            seg_len = CARD_REQUEST_SEGMENT_MAX_LEN

        port.write(req_json[seg_off:seg_off + seg_len]
                   .encode('utf-8'))
        seg_off += seg_len
        seg_left -= seg_len
        if seg_left == 0:
            break
        time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)


class Notecard:
    """Base Notecard class.

    Primary Notecard Class, which provides a shared __init__
    to reset the Notecard via Serial or I2C.
    """

    _user_agent = {
        'agent': 'note-python',
        'os_name': sys.implementation.name,
        'os_platform': sys.platform,
        'os_version': sys.version
    }
    _user_agent_sent = False

    def __init__(self):
        """Initialize the Notecard through a reset and configure user agent."""
        self.Reset()

        if sys.implementation.name == 'cpython':
            self._user_agent['os_family'] = os.name
        else:
            self._user_agent['os_family'] = os.uname().machine

    def _preprocessReq(self, req):
        """Inspect the request for hub.set and add the User Agent."""
        if 'hub.set' in req.values():
            # Merge the User Agent to send along with the hub.set request.
            new_req = req.copy()
            new_req.update(self.GetUserAgent())
            req = new_req

            self._user_agent_sent = True
        return req

    def GetUserAgent(self):
        """Return the User Agent String for the host for debug purposes."""
        return self._user_agent

    def UserAgentSent(self):
        """Return true if the User Agent has been sent to the Notecard."""
        return self._user_agent_sent


class OpenSerial(Notecard):
    """Notecard class for Serial communication."""

    def Command(self, req):
        """Perform a Notecard command and exit with no response."""
        req = self._preprocessReq(req)
        if 'cmd' not in req:
            raise Exception("Please use 'cmd' instead of 'req'")

        if use_serial_lock:
            try:
                self.lock.acquire(timeout=5)
                serialCommand(self.uart, req, self._debug)
            except Timeout:
                raise Exception("Notecard in use")
            finally:
                self.lock.release()
        else:
            serialCommand(self.uart, req, self._debug)

    def Transaction(self, req):
        """Perform a Notecard transaction and return the result."""
        req = self._preprocessReq(req)
        if use_serial_lock:
            try:
                self.lock.acquire(timeout=5)
                return serialTransaction(self.uart, req, self._debug)
            except Timeout:
                raise Exception("Notecard in use")
            finally:
                self.lock.release()
        else:
            return serialTransaction(self.uart, req, self._debug)

    def Reset(self):
        """Reset the Notecard."""
        if use_serial_lock:
            try:
                self.lock.acquire(timeout=5)
                serialReset(self.uart)
            except Timeout:
                raise Exception("Notecard in use")
            finally:
                self.lock.release()
        else:
            serialReset(self.uart)

    def __init__(self, uart_id, debug=False):
        """Initialize the Notecard before a reset."""
        self._user_agent['req_interface'] = 'serial'
        self._user_agent['req_port'] = str(uart_id)

        self.uart = uart_id
        self._debug = debug

        if use_serial_lock:
            self.lock = FileLock('serial.lock', timeout=1)
        super().__init__()


class OpenI2C(Notecard):
    """Notecard class for I2C communication."""

    def _sendPayload(self, json):
        chunk_offset = 0
        json_left = len(json)
        sent_in_seg = 0
        while json_left > 0:
            time.sleep(.001)
            chunk_len = min(json_left, self.max)
            reg = bytearray(1)
            reg[0] = chunk_len
            write_data = bytes(json[
                               chunk_offset:
                               chunk_offset + chunk_len
                               ], 'utf-8')
            if use_periphery:
                msgs = [I2C.Message(reg + write_data)]
                self.i2c.transfer(self.addr, msgs)
            else:
                self.i2c.writeto(self.addr, reg + write_data)
            chunk_offset += chunk_len
            json_left -= chunk_len
            sent_in_seg += chunk_len
            if sent_in_seg > CARD_REQUEST_SEGMENT_MAX_LEN:
                sent_in_seg -= CARD_REQUEST_SEGMENT_MAX_LEN
            time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS / 1000)

    def Command(self, req):
        """Perform a Notecard command and exit with no response."""
        req = self._preprocessReq(req)
        if 'cmd' not in req:
            raise Exception("Please use 'cmd' instead of 'req'")

        req_json = prepareRequest(req, self._debug)

        while not self.lock():
            pass

        try:
            self._sendPayload(req_json)
        finally:
            self.unlock()

    def Transaction(self, req):
        """Perform a Notecard transaction and return the result."""
        req = self._preprocessReq(req)

        req_json = prepareRequest(req, self._debug)
        rsp_json = ""

        while not self.lock():
            pass

        try:
            self._sendPayload(req_json)

            chunk_len = 0
            received_newline = False
            start = start_timeout()
            transaction_timeout_secs = 10
            while True:
                time.sleep(.001)
                reg = bytearray(2)
                reg[0] = 0
                reg[1] = chunk_len
                readlen = chunk_len + 2
                buf = bytearray(readlen)
                if use_periphery:
                    msgs = [I2C.Message(reg), I2C.Message(buf, read=True)]
                    self.i2c.transfer(self.addr, msgs)
                    buf = msgs[1].data
                elif use_micropython:
                    self.i2c.writeto(self.addr, reg, False)
                    self.i2c.readfrom_into(self.addr, buf)
                else:
                    self.i2c.writeto_then_readfrom(self.addr, reg, buf)
                available = buf[0]
                good = buf[1]
                data = buf[2:2 + good]
                if good > 0 and buf[-1] == 0x0a:
                    received_newline = True
                try:
                    rsp_json += "".join(map(chr, data))
                except:
                    pass
                chunk_len = min(available, self.max)
                if chunk_len > 0:
                    continue
                if received_newline:
                    break
                if (has_timed_out(start, transaction_timeout_secs)):
                    raise Exception("notecard request or response was lost")
                time.sleep(0.05)

        finally:
            self.unlock()

        if self._debug:
            print(rsp_json.rstrip())
        rsp = json.loads(rsp_json)
        return rsp

    def Reset(self):
        """Reset the Notecard."""
        chunk_len = 0

        while not self.lock():
            pass

        try:
            while True:
                time.sleep(.001)
                reg = bytearray(2)
                reg[0] = 0
                reg[1] = chunk_len
                readlen = chunk_len + 2
                buf = bytearray(readlen)
                if use_periphery:
                    msgs = [I2C.Message(reg), I2C.Message(buf, read=True)]
                    self.i2c.transfer(self.addr, msgs)
                    buf = msgs[1].data
                elif use_micropython:
                    self.i2c.writeto(self.addr, reg, False)
                    self.i2c.readfrom_into(self.addr, buf)
                else:
                    self.i2c.writeto_then_readfrom(self.addr, reg, buf)
                available = buf[0]
                if available == 0:
                    break
                chunk_len = min(available, self.max)
        finally:
            self.unlock()

        pass

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
        super().__init__()
