import os
import sys
import serial
import periphery
import pytest

from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402
from notecard import service  # noqa: E402


def get_serial_and_port():
    serial = Mock()  # noqa: F811
    port = serial.Serial("/dev/tty.foo", 9600)
    port.read.side_effect = [b'\r', b'\n', None]

    card = notecard.OpenSerial(port)

    return (card, port)


def get_i2c_and_port():
    periphery = Mock()  # noqa: F811
    port = periphery.I2C("dev/i2c-foo")
    port.try_lock.return_value = True

    card = notecard.OpenI2C(port, 0x17, 255)

    return (card, port)


def test_open_serial():
    card, _ = get_serial_and_port()

    assert card.uart is not None


def test_open_i2c():
    card, _ = get_i2c_and_port()

    assert card.i2c is not None


def test_transaction():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{\"connected\":true}\r\n"]

    response = card.Transaction({"req": "service.status"})

    assert "connected" in response
    assert response["connected"] is True


def test_service_set():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{}\r\n"]

    response = service.set(card, product="com.blues.tester",
                           sn="foo",
                           mode="continuous",
                           minutes=2,
                           hours=1,
                           sync=True)

    assert response == {}


def test_service_set_invalid_card():
    with pytest.raises(Exception, match="Notecard object required"):
        service.set(None, product="com.blues.tester")


def test_service_sync():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{}\r\n"]

    response = service.sync(card)

    assert response == {}


def test_service_sync_status():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{\"status\":\"connected\"}\r\n"]

    response = service.syncStatus(card)

    assert "status" in response
    assert response["status"] == "connected"


def test_service_status():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{\"connected\":true}\r\n"]

    response = service.status(card)

    assert "connected" in response
    assert response["connected"] is True


def test_service_log():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{}\r\n"]

    response = service.log(card, "there's been an issue!", False)

    assert response == {}


def test_service_get():
    card, port = get_serial_and_port()

    port.read.side_effect = [char.encode('utf-8')
                             for char in "{\"mode\":\"continuous\"}\r\n"]

    response = service.get(card)

    assert "mode" in response
    assert response["mode"] == "continuous"

