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
import json
import time

use_periphery = False
use_serial_lock = False
if sys.implementation.name == 'cpython':
    if sys.platform == "linux" or sys.platform == "linux2":
        use_periphery = True
        from periphery import I2C

        use_serial_lock = True
        from filelock import Timeout, FileLock

NOTECARD_I2C_ADDRESS = 0x17

# The notecard is a real-time device that has a fixed size interrupt buffer.
# We can push data at it far, far faster than it can process it,
# therefore we push it in segments with a pause between each segment.
CARD_REQUEST_SEGMENT_MAX_LEN = 250
CARD_REQUEST_SEGMENT_DELAY_MS = 250


def serialReadByte(port):
    """Read a single byte from a Notecard."""
    if sys.implementation.name == 'micropython':
        if not port.any():
            return None
    elif sys.implementation.name == 'cpython':
        if use_periphery:
            if port.input_waiting() == 0:
                return None
        else:
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
    req_json = json.dumps(req)
    if debug:
        print(req_json)
    req_json += "\n"

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

    rsp_json = ""
    while True:
        data = serialReadByte(port)
        if data is None:
            continue
        try:
            data_string = data.decode('utf-8')
            if data_string == "\n":
                break
            rsp_json += data_string
        except:
            pass
    if debug:
        print(rsp_json.rstrip())
    rsp = json.loads(rsp_json)
    return rsp


def serialCommand(port, req, debug):
    """Perform a single write to and read from a Notecard."""
    req_json = json.dumps(req)
    if debug:
        print(req_json)
    req_json += "\n"

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

    def __init__(self):
        """Initialize the Notecard through a reset."""
        self.Reset()


class OpenSerial(Notecard):
    """Notecard class for Serial communication."""

    def Request(self, req):
        """Call the Transaction method and discard the result."""
        self.Transaction(req)
        return True

    def RequestResponse(self, req):
        """Call the Transaction method and return the result."""
        return self.Transaction(req)

    def Command(self, req):
        """Perform a Notecard command and exit with no response."""
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
        self.uart = uart_id
        self._debug = debug

        if use_serial_lock:
            self.lock = FileLock('serial.lock', timeout=1)
        super().__init__()


class OpenI2C(Notecard):
    """Notecard class for I2C communication."""

    def Transaction(self, req):
        """Perform a Notecard transaction and return the result."""
        req_json = json.dumps(req)
        if self._debug:
            print(req_json)

        req_json += "\n"
        rsp_json = ""

        while not self.lock():
            pass

        try:
            chunk_offset = 0
            json_left = len(req_json)
            sent_in_seg = 0
            while json_left > 0:
                time.sleep(.001)
                chunk_len = min(json_left, self.max)
                reg = bytearray(1)
                reg[0] = chunk_len
                write_data = bytes(req_json[
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

            chunk_len = 0
            received_newline = False
            start = time.time()
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
                if (time.time() >= start + transaction_timeout_secs):
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
        if not use_periphery:
            return self.i2c.try_lock()
        return True

    def unlock(self):
        """Unlock the I2C port."""
        if not use_periphery:
            return self.i2c.unlock()
        return True

    def __init__(self, i2c, address, max_transfer, debug=False):
        """Initialize the Notecard before a reset."""
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
