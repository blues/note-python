import os
import sys
import serial

from unittest.mock import Mock, MagicMock, patch

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402

def test_open_serial():
    serial = Mock()
    port = serial.Serial("/dev/tty.foo", 9600)
    port.read.side_effect = [b'\r', b'\n', None]

    card = notecard.OpenSerial(port)
    
    assert card.uart is not None
