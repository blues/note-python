import os
import sys
import serial
import periphery
import pytest

from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

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


def test_open_serial():
    nCard, _ = get_serial_and_port()

    assert nCard.uart is not None


def test_open_i2c():
    nCard, _ = get_i2c_and_port()

    assert nCard.i2c is not None


def test_transaction():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"connected\":true}\r\n"
    print(port.readline())
    response = nCard.Transaction({"req": "hub.status"})

    assert "connected" in response
    assert response["connected"] is True


def test_command():
    nCard, port = get_serial_and_port()

    response = nCard.Command({"cmd": "card.sleep"})

    assert response is None


def test_command_fail_if_req():
    nCard, port = get_serial_and_port()

    with pytest.raises(Exception, match="Please use 'cmd' instead of 'req'"):
        nCard.Command({"req": "card.sleep"})


def test_hub_set():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"
    response = hub.set(nCard, product="com.blues.tester",
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


def test_hub_set_invalid_card():
    with pytest.raises(Exception, match="Notecard object required"):
        hub.set(None, product="com.blues.tester")


def test_hub_sync():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"
    response = hub.sync(nCard)

    assert response == {}


def test_hub_sync_status():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"status\":\"connected\"}\r\n"

    response = hub.syncStatus(nCard, True)

    assert "status" in response
    assert response["status"] == "connected"


def test_hub_status():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"connected\":true}\r\n"

    response = hub.status(nCard)

    assert "connected" in response
    assert response["connected"] is True


def test_hub_log():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = hub.log(nCard, "there's been an issue!", False)

    assert response == {}


def test_hub_get():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"mode\":\"continuous\"}\r\n"

    response = hub.get(nCard)

    assert "mode" in response
    assert response["mode"] == "continuous"


def test_card_time():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"time\":1592490375}\r\n"

    response = card.time(nCard)

    assert "time" in response
    assert response["time"] == 1592490375


def test_card_status():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"usb\":true,\"status\":\"{normal}\"}\r\n"

    response = card.status(nCard)

    assert "status" in response
    assert response["status"] == "{normal}"


def test_card_temp():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"value\":33.625,\"calibration\":-3.0}\r\n"

    response = card.temp(nCard, minutes=20)

    assert "value" in response
    assert response["value"] == 33.625


def test_card_attn():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"set\":true}\r\n"

    response = card.attn(nCard, mode="arm, files",
                         files=["sensors.qo"],
                         seconds=10, payload={"foo": "bar"},
                         start=True)

    assert "set" in response
    assert response["set"] is True


def test_card_attn_with_invalid_card():
    with pytest.raises(Exception, match="Notecard object required"):
        card.attn(None, mode="arm")


def test_card_voltage():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"hours\":707}\r\n"

    response = card.voltage(nCard, hours=24, offset=5, vmax=4, vmin=3)

    assert "hours" in response
    assert response["hours"] == 707


def test_card_wireless():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"status\":\"{modem-off}\",\"count\":1}\r\n"

    response = card.wireless(nCard, mode="auto", apn="-")

    assert "status" in response
    assert response["status"] == "{modem-off}"


def test_card_version():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"version\":\"notecard-1.2.3.9950\"}\r\n"

    response = card.version(nCard)

    assert "version" in response
    assert response["version"] == "notecard-1.2.3.9950"


def test_note_add():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"total\":1}\r\n"

    response = note.add(nCard, file="sensors.qo",
                        body={"temp": 72.22},
                        payload="b64==",
                        sync=True)

    assert "total" in response
    assert response["total"] == 1


def test_note_get():
    nCard, port = get_serial_and_port()

    port.readline.return_value = \
        "{\"note\":\"s\",\"body\":{\"s\":\"foo\"}}\r\n"

    response = note.get(nCard, file="settings.db",
                        note_id="s",
                        delete=True,
                        deleted=False)

    assert "note" in response
    assert response["note"] == "s"


def test_note_delete():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = note.delete(nCard, file="settings.db", note_id="s")

    assert response == {}


def test_note_update():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = note.update(nCard, file="settings.db", note_id="s",
                           body={"foo": "bar"}, payload="123dfb==")

    assert response == {}


def test_note_changes():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"changes\":5,\"total\":15}\r\n"

    response = note.changes(nCard, file="sensors.qo",
                            tracker="123",
                            maximum=10,
                            start=True,
                            stop=False,
                            deleted=False,
                            delete=True)

    assert "changes" in response
    assert response["changes"] == 5


def test_note_template():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"bytes\":40}\r\n"

    response = note.template(nCard, file="sensors.qo",
                             body={"temp": 1.1, "hu": 1},
                             length=5)

    assert "bytes" in response
    assert response["bytes"] == 40


def test_debug_mode_on_serial():
    serial = Mock()  # noqa: F811
    port = serial.Serial("/dev/tty.foo", 9600)
    port.read.side_effect = [b'\r', b'\n', None]

    nCard = notecard.OpenSerial(port, debug=True)

    assert nCard._debug


def test_debug_mode_on_i2c():
    periphery = Mock()  # noqa: F811
    port = periphery.I2C("dev/i2c-foo")
    port.try_lock.return_value = True

    nCard = notecard.OpenI2C(port, 0x17, 255, debug=True)

    assert nCard._debug


def test_env_default():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = env.default(nCard, name="pump", text="on")

    assert response == {}


def test_env_set():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = env.set(nCard, name="pump", text="on")

    assert response == {}


def test_env_get():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = env.get(nCard, name="pump")

    assert response == {}


def test_env_modified():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"time\": 1605814493}\r\n"

    response = env.modified(nCard)

    assert "time" in response
    assert response["time"] == 1605814493


def test_file_delete():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{}\r\n"

    response = file.delete(nCard, files=["sensors.qo"])

    assert response == {}


def test_file_changes():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"total\":5}\r\n"

    response = file.changes(nCard, tracker="123", files=["sensors.qo"])

    assert "total" in response
    assert response["total"] == 5


def test_file_stats():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"total\":24}\r\n"

    response = file.stats(nCard)

    assert "total" in response
    assert response["total"] == 24


def test_file_pendingChanges():
    nCard, port = get_serial_and_port()

    port.readline.return_value = "{\"changes\":1}\r\n"

    response = file.pendingChanges(nCard)

    assert "changes" in response
    assert response["changes"] == 1
