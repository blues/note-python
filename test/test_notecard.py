import os
import sys
import pytest
from unittest.mock import Mock, MagicMock, patch
import periphery
import json

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402
from notecard import card, hub, note, env, file  # noqa: E402


def get_serial_and_port():
    serial = Mock()  # noqa: F811
    port = serial.Serial("/dev/tty.foo", 9600)
    port.read.side_effect = [b'\r', b'\n', None]
    port.readline.return_value = "\r\n"

    nCard = notecard.OpenSerial(port)

    return (nCard, port)


def get_i2c_and_port():
    periphery = Mock()  # noqa: F811
    port = periphery.I2C("dev/i2c-foo")
    port.try_lock.return_value = True

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

    def test_hub_set(self):
        nCard, port = self.get_port("{}\r\n")

        response = hub.set(nCard,
                           product="com.blues.tester",
                           sn="foo",
                           mode="continuous",
                           outbound=2,
                           inbound=60,
                           duration=5,
                           sync=True,
                           align=True,
                           voutbound="2.3",
                           vinbound="3.3",
                           host="http://hub.blues.foo")

        assert response == {}

    def test_user_agent_sent_is_false_before_hub_set(self):
        nCard, _ = self.get_port()

        assert nCard.UserAgentSent() is False

    def test_send_user_agent_in_hub_set_helper(self):
        nCard, port = self.get_port("{}\r\n")

        hub.set(nCard,
                product="com.blues.tester",
                sn="foo",
                mode="continuous",
                outbound=2,
                inbound=60,
                duration=5,
                sync=True,
                align=True,
                voutbound="2.3",
                vinbound="3.3",
                host="http://hub.blues.foo")

        assert nCard.UserAgentSent() is True

    def test_send_user_agent_in_hub_set_transaction(self):
        nCard, port = self.get_port("{\"connected\":true}\r\n")

        nCard.Transaction({"req": "hub.set"})

        assert nCard.UserAgentSent() is True

    def test_hub_set_invalid_card(self):
        with pytest.raises(Exception, match="Notecard object required"):
            hub.set(None, product="com.blues.tester")

    def test_hub_sync(self):
        nCard, port = self.get_port("{}\r\n")

        response = hub.sync(nCard)

        assert response == {}

    def test_hub_sync_status(self):
        nCard, port = self.get_port("{\"status\":\"connected\"}\r\n")

        response = hub.syncStatus(nCard, True)

        assert "status" in response
        assert response["status"] == "connected"

    def test_hub_status(self):
        nCard, port = self.get_port("{\"connected\":true}\r\n")

        response = hub.status(nCard)

        assert "connected" in response
        assert response["connected"] is True

    def test_hub_log(self):
        nCard, port = self.get_port("{}\r\n")

        response = hub.log(nCard, "there's been an issue!", False)

        assert response == {}

    def test_hub_get(self):
        nCard, port = self.get_port("{\"mode\":\"continuous\"}\r\n")

        response = hub.get(nCard)

        assert "mode" in response
        assert response["mode"] == "continuous"

    def test_card_time(self):
        nCard, port = self.get_port("{\"time\":1592490375}\r\n")

        response = card.time(nCard)

        assert "time" in response
        assert response["time"] == 1592490375

    def test_card_status(self):
        nCard, port = self.get_port(
            "{\"usb\":true,\"status\":\"{normal}\"}\r\n")

        response = card.status(nCard)

        assert "status" in response
        assert response["status"] == "{normal}"

    def test_card_temp(self):
        nCard, port = self.get_port(
            "{\"value\":33.625,\"calibration\":-3.0}\r\n")

        response = card.temp(nCard, minutes=20)

        assert "value" in response
        assert response["value"] == 33.625

    def test_card_attn(self):
        nCard, port = self.get_port("{\"set\":true}\r\n")

        response = card.attn(nCard,
                             mode="arm, files",
                             files=["sensors.qo"],
                             seconds=10,
                             payload={"foo": "bar"},
                             start=True)

        assert "set" in response
        assert response["set"] is True

    def test_card_attn_with_invalid_card(self):
        with pytest.raises(Exception, match="Notecard object required"):
            card.attn(None, mode="arm")

    def test_card_voltage(self):
        nCard, port = self.get_port("{\"hours\":707}\r\n")

        response = card.voltage(nCard, hours=24, offset=5, vmax=4, vmin=3)

        assert "hours" in response
        assert response["hours"] == 707

    def test_card_wireless(self):
        nCard, port = self.get_port(
            "{\"status\":\"{modem-off}\",\"count\":1}\r\n")

        response = card.wireless(nCard, mode="auto", apn="-")

        assert "status" in response
        assert response["status"] == "{modem-off}"

    def test_card_version(self):
        nCard, port = self.get_port(
            "{\"version\":\"notecard-1.2.3.9950\"}\r\n")

        response = card.version(nCard)

        assert "version" in response
        assert response["version"] == "notecard-1.2.3.9950"

    def test_note_add(self):
        nCard, port = self.get_port("{\"total\":1}\r\n")

        response = note.add(nCard,
                            file="sensors.qo",
                            body={"temp": 72.22},
                            payload="b64==",
                            sync=True)

        assert "total" in response
        assert response["total"] == 1

    def test_note_get(self):
        nCard, port = self.get_port(
            "{\"note\":\"s\",\"body\":{\"s\":\"foo\"}}\r\n")

        response = note.get(nCard,
                            file="settings.db",
                            note_id="s",
                            delete=True,
                            deleted=False)

        assert "note" in response
        assert response["note"] == "s"

    def test_note_delete(self):
        nCard, port = self.get_port("{}\r\n")

        response = note.delete(nCard, file="settings.db", note_id="s")

        assert response == {}

    def test_note_update(self):
        nCard, port = self.get_port("{}\r\n")

        response = note.update(nCard,
                               file="settings.db",
                               note_id="s",
                               body={"foo": "bar"},
                               payload="123dfb==")

        assert response == {}

    def test_note_changes(self):
        nCard, port = self.get_port("{\"changes\":5,\"total\":15}\r\n")

        response = note.changes(nCard,
                                file="sensors.qo",
                                tracker="123",
                                maximum=10,
                                start=True,
                                stop=False,
                                deleted=False,
                                delete=True)

        assert "changes" in response
        assert response["changes"] == 5

    def test_note_template(self):
        nCard, port = self.get_port("{\"bytes\":40}\r\n")

        response = note.template(nCard,
                                 file="sensors.qo",
                                 body={
                                     "temp": 1.1,
                                     "hu": 1
                                 },
                                 length=5)

        assert "bytes" in response
        assert response["bytes"] == 40

    def test_env_default(self):
        nCard, port = self.get_port("{}\r\n")

        response = env.default(nCard, name="pump", text="on")

        assert response == {}

    def test_env_set(self):
        nCard, port = self.get_port("{}\r\n")

        response = env.set(nCard, name="pump", text="on")

        assert response == {}

    def test_env_get(self):
        nCard, port = self.get_port("{}\r\n")

        response = env.get(nCard, name="pump")

        assert response == {}

    def test_env_modified(self):
        nCard, port = self.get_port("{\"time\": 1605814493}\r\n")

        response = env.modified(nCard)

        assert "time" in response
        assert response["time"] == 1605814493

    def test_file_delete(self):
        nCard, port = self.get_port("{}\r\n")

        response = file.delete(nCard, files=["sensors.qo"])

        assert response == {}

    def test_file_changes(self):
        nCard, port = self.get_port("{\"total\":5}\r\n")

        response = file.changes(nCard, tracker="123", files=["sensors.qo"])

        assert "total" in response
        assert response["total"] == 5

    def test_file_stats(self):
        nCard, port = self.get_port("{\"total\":24}\r\n")

        response = file.stats(nCard)

        assert "total" in response
        assert response["total"] == 24

    def test_file_pendingChanges(self):
        nCard, port = self.get_port("{\"changes\":1}\r\n")

        response = file.pendingChanges(nCard)

        assert "changes" in response
        assert response["changes"] == 1

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
        serial = Mock()  # noqa: F811
        port = serial.Serial("/dev/tty.foo", 9600)
        port.read.side_effect = [b'\r', b'\n', None]

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
