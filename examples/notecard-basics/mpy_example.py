"""note-python MicroPython example.

This file contains a complete working sample for using the note-python
library on a MicroPython device.
"""
import sys
import time
import notecard
import board

if sys.implementation.name != "micropython":
    raise Exception("Please run this example in a MicroPython environment.")

from machine import UART  # noqa: E402
from machine import I2C  # noqa: E402
from machine import Pin


def configure_notecard(card, product_uid):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req = {"req": "hub.set"}
    req["product"] = product_uid
    req["mode"] = "continuous"

    card.Transaction(req)


def get_temp_and_voltage(card):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req = {"req": "card.temp"}
    rsp = card.Transaction(req)
    temp = rsp["value"]

    req = {"req": "card.voltage"}
    rsp = card.Transaction(req)
    voltage = rsp["value"]

    return temp, voltage


def run_example(product_uid, use_uart=True):
    """Connect to Notcard and run a transaction test."""
    print("Opening port...")
    if use_uart:
        port = UART(board.UART, 9600)
        port.init(9600, bits=8, parity=None, stop=1,
                  timeout=3000, timeout_char=100)
    else:
        port = I2C(board.I2C_ID, scl=Pin(board.SCL), sda=Pin(board.SDA))

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
