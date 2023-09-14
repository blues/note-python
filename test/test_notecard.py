import os
import sys
import pytest
from unittest.mock import Mock, MagicMock, patch
import periphery
import json

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402


def get_serial_and_port():
    serial = Mock()  # noqa: F811
    port = serial.Serial("/dev/tty.foo", 9600)
    port.read.side_effect = [b'\r', b'\n', None]
    port.readline.return_value = "\r\n"

    # Patch the Reset method so that we don't actually call it during __init__.
    with patch('notecard.notecard.OpenSerial.Reset'):
        nCard = notecard.OpenSerial(port)

    return (nCard, port)


def get_i2c_and_port():
    periphery = Mock()  # noqa: F811
    port = periphery.I2C("dev/i2c-foo")
    port.try_lock.return_value = True

    # Patch the Reset method so that we don't actually call it during __init__.
    with patch('notecard.notecard.OpenI2C.Reset'):
        nCard = notecard.OpenI2C(port, 0x17, 255)

    return (nCard, port)


class NotecardTest:

    def test_get_user_agent(self):
        nCard, _ = self.get_port()
        userAgent = nCard.GetUserAgent()

        assert userAgent['agent'] == 'note-python'
        assert userAgent['os_name'] is not None
        assert userAgent['os_platform'] is not None
        assert userAgent['os_version'] is not None
        assert userAgent['os_family'] is not None

    def test_transaction(self):
        nCard, port = self.get_port("{\"connected\":true}\r\n")

        response = nCard.Transaction({"req": "hub.status"})

        assert "connected" in response
        assert response["connected"] is True

    @patch('notecard.notecard.TransactionManager')
    def test_setting_transaction_pins(self, transaction_manager_mock):
        nCard, _ = self.get_port("{\"connected\":true}\r\n")

        nCard.SetTransactionPins(1, 2)
        nCard.Transaction({"req": "hub.status"})

        # If transaction pins have been set, start and stop should be called
        # once for each Transaction call.
        nCard._transaction_manager.start.assert_called_once()
        nCard._transaction_manager.stop.assert_called_once()

    def test_command(self):
        nCard, port = self.get_port()

        response = nCard.Command({"cmd": "card.sleep"})

        assert response is None

    def test_command_fail_if_req(self):
        nCard, port = self.get_port()

        with pytest.raises(Exception,
                           match="Please use 'cmd' instead of 'req'"):
            nCard.Command({"req": "card.sleep"})

    def test_user_agent_sent_is_false_before_hub_set(self):
        nCard, _ = self.get_port()

        assert nCard.UserAgentSent() is False

    def test_send_user_agent_in_hub_set_transaction(self):
        nCard, port = self.get_port("{\"connected\":true}\r\n")

        nCard.Transaction({"req": "hub.set"})

        assert nCard.UserAgentSent() is True

    def get_port(self, response=None):
        raise NotImplementedError("subclasses must implement `get_port()`")


class TestNotecardMockSerial(NotecardTest):

    def get_port(self, response=None):
        nCard, port = get_serial_and_port()
        if response is not None:
            port.readline.return_value = response
        return (nCard, port)

    def test_user_agent_is_serial_when_serial_used(self):
        nCard, _ = self.get_port()
        userAgent = nCard.GetUserAgent()

        assert userAgent['req_interface'] == 'serial'
        assert userAgent['req_port'] is not None

    def test_open_serial(self):
        nCard, _ = get_serial_and_port()

        assert nCard.uart is not None

    def test_debug_mode_on_serial(self):
        # Patch the Reset method so that we don't actually call it during
        # __init__.
        with patch('notecard.notecard.OpenSerial.Reset'):
            port = MagicMock()
            nCard = notecard.OpenSerial(port, debug=True)

        assert nCard._debug


class TestNotecardMockI2C(NotecardTest):

    def get_port(self, response=None):
        nCard, port = get_i2c_and_port()
        if response is not None:
            chunklen = 0
            tosend = bytes(response, 'utf-8')

            def writeto_then_readfrom(addr, write, read):
                nonlocal chunklen, tosend
                read[0] = len(tosend)
                read[1] = chunklen
                read[2:2 + chunklen] = tosend[0:chunklen]
                tosend = tosend[chunklen:]
                chunklen = len(tosend)

            def transfer(addr, messages: periphery.I2C.Message):
                if len(messages) == 2 and messages[1].read:
                    read = messages[1].data
                    writeto_then_readfrom(addr, messages[0].data, read)

            port.writeto_then_readfrom = writeto_then_readfrom
            port.transfer = transfer
        return (nCard, port)

    def test_open_i2c(self):
        nCard, _ = get_i2c_and_port()

        assert nCard.i2c is not None

    def test_user_agent_is_i2c_when_i2c_used(self):
        nCard, _ = self.get_port()
        userAgent = nCard.GetUserAgent()

        assert userAgent['req_interface'] == 'i2c'
        assert userAgent['req_port'] is not None

    def test_debug_mode_on_i2c(self):
        periphery = Mock()  # noqa: F811
        port = periphery.I2C("dev/i2c-foo")
        port.try_lock.return_value = True

        nCard = notecard.OpenI2C(port, 0x17, 255, debug=True)

        assert nCard._debug


class MockNotecard(notecard.Notecard):

    def Reset(self):
        pass


class TestUserAgent:

    def setUserAgentInfo(self, info=None):
        nCard = MockNotecard()
        orgReq = {"req": "hub.set"}
        nCard.SetAppUserAgent(info)
        req = json.loads(nCard._prepare_request(orgReq))
        return req

    def test_amends_hub_set_request(self):
        req = self.setUserAgentInfo()
        assert req['body'] is not None

    def test_adds_app_info(self):
        info = {"app": "myapp"}
        req = self.setUserAgentInfo(info)
        assert req['body']['app'] == 'myapp'
