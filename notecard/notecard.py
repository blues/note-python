
import sys
import json
import time

use_periphery = False
if sys.implementation.name == 'cpython':
    if sys.platform == "linux" or sys.platform == "linux2":
        use_periphery = True
        from periphery import I2C

NOTECARD_I2C_ADDRESS    = 0x17
notecardDebug           = True

# The notecard is a real-time device that has a fixed size interrupt buffer.  We can push data
# at it far, far faster than it can process it, therefore we push it in segments with a pause
# between each segment.
CARD_REQUEST_SEGMENT_MAX_LEN = 1000
CARD_REQUEST_SEGMENT_DELAY_MS = 250

def serialReadByte(port):
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

class Notecard:

    def __init__(self):
        self.Reset()

class OpenSerial(Notecard):

    def Request(self, req):
        self.Transaction(self, req)
        return True

    def RequestResponse(self, req):
        return self.Transaction(self, req)

    def Transaction(self, req):
        req_json = json.dumps(req) 
        if notecardDebug:
            print(req_json)
        req_json += "\n"

        seg_off = 0
        seg_left = len(req_json)
        while True:
            seg_len = seg_left
            if seg_len > CARD_REQUEST_SEGMENT_MAX_LEN:
                seg_len = CARD_REQUEST_SEGMENT_MAX_LEN
            self.uart.write(req_json[seg_off:seg_off+seg_len].encode('utf-8'))
            seg_off += seg_len
            seg_left -= seg_len
            if seg_left == 0:
                break
            time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS/1000)

        rsp_json = ""
        while True:
            data = serialReadByte(self.uart)
            if data is None:
                continue
            try:
                data_string = data.decode('utf-8')
                if data_string == "\n":
                    break
                rsp_json += data_string
            except:
                pass
        if notecardDebug:
            print(rsp_json.rstrip())
        rsp = json.loads(rsp_json)
        return rsp

    def Reset(self):
        for i in range(10):
            try:
                self.uart.write(b'\n\n')
            except:
                continue
            time.sleep(0.5)
            somethingFound = False
            nonControlCharFound = False
            while True:
                data = serialReadByte(self.uart)
                if data is None:
                    break
                somethingFound = True
                if data[0] >= 0x20:
                    nonControlCharFound = True
            if somethingFound and not nonControlCharFound:
                break
        else:
            raise Exception("Notecard not responding")

    def __init__(self, uart_id):
        self.uart = uart_id
        super().__init__()

class OpenI2C(Notecard):

    def Transaction(self, req):

        req_json = json.dumps(req)
        if notecardDebug:
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
                write_data = bytes(req_json[chunk_offset:chunk_offset+chunk_len], 'utf-8')
                if use_periphery:
                    msgs = [I2C.Message(reg+write_data)]
                    self.i2c.transfer(self.addr, msgs)
                else:
                    self.i2c.writeto(self.addr, reg, stop=False)
                    self.i2c.writeto(self.addr, write_data, stop=True)
                chunk_offset += chunk_len
                json_left -= chunk_len
                sent_in_seg += chunk_len
                if sent_in_seg > CARD_REQUEST_SEGMENT_MAX_LEN:
                    sent_in_seg -= CARD_REQUEST_SEGMENT_MAX_LEN
                    time.sleep(CARD_REQUEST_SEGMENT_DELAY_MS/1000)
                    
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
                    self.i2c.writeto(self.addr, reg, stop=False)
                    self.i2c.readfrom_into(self.addr, buf)
                available = buf[0]
                good = buf[1]
                data = buf[2:2+good]
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

        if notecardDebug:
            print(rsp_json.rstrip())
        rsp = json.loads(rsp_json)
        return rsp

    def Reset(self):
        chunk_len = 0
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
                self.i2c.writeto(self.addr, reg, stop=False)
                self.i2c.readfrom_into(self.addr, buf)
            available = buf[0]
            if available == 0:
                break
            chunk_len = min(available, self.max)
        pass

    def lock(self):
        if not use_periphery:
            return self.i2c.try_lock()
        return True

    def unlock(self):
        if not use_periphery:
            return self.i2c.unlock()
        return True

    def __init__(self, i2c, address, max_transfer):
        self.i2c = i2c
        if address == 0:
            self.addr = NOTECARD_I2C_ADDRESS
        else:
            self.addr = address
        if max_transfer == 0:
            self.max = 255
        else:
            self.max = max_transfer
        super().__init__()
