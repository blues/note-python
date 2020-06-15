import os
import sys
import serial
import periphery

from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402


def test_open_serial():
    serial = Mock()  # noqa: F811
    port = serial.Serial("/dev/tty.foo", 9600)
    port.read.side_effect = [b'\r', b'\n', None]

    card = notecard.OpenSerial(port)

    assert card.uart is not None


def test_open_i2c():
    periphery = Mock()  # noqa: F811
    port = periphery.I2C("dev/i2c-foo")
    port.try_lock.return_value = True

    card = notecard.OpenI2C(port, 0x17, 255)

    assert card.i2c is not None
