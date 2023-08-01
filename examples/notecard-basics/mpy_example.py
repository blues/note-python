"""note-python MicroPython example.

This file contains a complete working sample for using the note-python
library on a MicroPython device.
"""
import sys
import time
import notecard

if sys.implementation.name != "micropython":
    raise Exception("Please run this example in a MicroPython environment.")

from machine import UART  # noqa: E402
from machine import I2C  # noqa: E402
from machine import Pin


def NotecardExceptionInfo(exception):
    """Construct a formatted Exception string.

    Args:
        exception (Exception): An exception object.

    Returns:
        string: a summary of the exception with line number and details.
    """
    name = exception.__class__.__name__
    return sys.platform + ": " + name + ": " \
        + " ".join(map(str, exception.args))


def configure_notecard(card, product_uid):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req = {"req": "hub.set"}
    req["product"] = product_uid
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


def run_example(product_uid, use_uart=True):
    """Connect to Notcard and run a transaction test."""
    print("Opening port...")
    if use_uart:
        port = UART(2, 9600)
        port.init(9600, bits=8, parity=None, stop=1,
                  timeout=3000, timeout_char=100)
    else:
        # If you"re using an ESP32, connect GPIO 22 to SCL and GPIO 21 to SDA.
        if "ESP32" in sys.implementation._machine:
            port = I2C(1, scl=Pin(22), sda=Pin(21))
        else:
            port = I2C()

    print("Opening Notecard...")
    if use_uart:
        card = notecard.OpenSerial(port, debug=True)
    else:
        card = notecard.OpenI2C(port, 0, 0, debug=True)

    # If success, configure the Notecard and send some data
    configure_notecard(card, product_uid)
    temp, voltage = get_temp_and_voltage(card)

    req = {"req": "note.add"}
    req["sync"] = True
    req["body"] = {"temp": temp, "voltage": voltage}

    card.Transaction(req)

    # Developer note: do not modify the line below, as we use this as to signify
    # that the example ran successfully to completion. We then use that to
    # determine pass/fail for certain tests that leverage these examples.
    print("Example complete.")


if __name__ == "__main__":
    product_uid = "com.your-company.your-project"
    # Choose either UART or I2C for Notecard
    use_uart = True
    run_example(product_uid, use_uart)
