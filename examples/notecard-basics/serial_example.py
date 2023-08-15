"""note-python Serial example.

This file contains a complete working sample for using the note-python
library with a Serial Notecard connection.
"""
import sys
import os
import time

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402

productUID = "com.your-company.your-project"

# For UART and I2C IO
if sys.implementation.name != 'cpython':
    raise Exception("Please run this example in a CPython environment.")

import serial  # noqa: E402


def NotecardExceptionInfo(exception):
    """Construct a formatted Exception string.

    Args:
        exception (Exception): An exception object.

    Returns:
        string: a summary of the exception with line number and details.
    """
    s1 = '{}'.format(sys.exc_info()[-1].tb_lineno)
    s2 = exception.__class__.__name__
    return "line " + s1 + ": " + s2 + ": " + ' '.join(map(str, exception.args))


def configure_notecard(card):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req = {"req": "hub.set"}
    req["product"] = productUID
    req["mode"] = "continuous"

    try:
        card.Transaction(req)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)


def get_temp_and_voltage(card):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    temp = 0
    voltage = 0

    try:
        req = {"req": "card.temp"}
        rsp = card.Transaction(req)
        temp = rsp["value"]

        req = {"req": "card.voltage"}
        rsp = card.Transaction(req)
        voltage = rsp["value"]
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)

    return temp, voltage


def main():
    """Connect to Notcard and run a transaction test."""
    print("Opening port...")
    try:
        if sys.platform == "linux" or sys.platform == "linux2":
            port = serial.Serial(port="/dev/serial0",
                                 baudrate=9600)
        elif sys.platform == "darwin":
            port = serial.Serial(port="/dev/tty.usbmodemNOTE1",
                                 baudrate=9600)
        elif sys.platform == "win32":
            port = serial.Serial(port="COM21",
                                 baudrate=9600)
    except Exception as exception:
        raise Exception("error opening port: "
                        + NotecardExceptionInfo(exception))

    print("Opening Notecard...")
    try:
        card = notecard.OpenSerial(port)
    except Exception as exception:
        raise Exception("error opening notecard: "
                        + NotecardExceptionInfo(exception))

    # If success, configure the Notecard and send some data
    configure_notecard(card)
    temp, voltage = get_temp_and_voltage(card)

    req = {"req": "note.add"}
    req["sync"] = True
    req["body"] = {"temp": temp, "voltage": voltage}

    try:
        card.Transaction(req)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)


main()
