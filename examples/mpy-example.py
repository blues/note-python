"""note-python MicroPython example.

This file contains a complete working sample for using the note-python
library on a MicroPython device.
"""
import sys
import time
import notecard

# Choose either UART or I2C for Notecard
use_uart = True

if sys.implementation.name != 'micropython':
    raise Exception("Please run this example in a MicroPython environment.")

from machine import UART  # noqa: E402
from machine import I2C  # noqa: E402


def NotecardExceptionInfo(exception):
    """Construct a formatted Exception string.

    Args:
        exception (Exception): An exception object.

    Returns:
        string: a summary of the exception with line number and details.
    """
    name = exception.__class__.__name__
    return sys.platform + ": " + name + ": " \
        + ' '.join(map(str, exception.args))


def transactionTest(card):
    """Submit a simple JSON-based request to the Notecard.

    Args:
        card (object): An instance of the Notecard class

    """
    req = {"req": "card.status"}

    try:
        rsp = card.Transaction(req)
        print(rsp)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)


def main():
    """Connect to Notcard and run a transaction test."""
    print("Opening port...")
    try:
        if use_uart:
            port = UART(2, 9600)
            port.init(9600, bits=8, parity=None, stop=1)
        else:
            port = I2C()
    except Exception as exception:
        raise Exception("error opening port: "
                        + NotecardExceptionInfo(exception))

    print("Opening Notecard...")
    try:
        if use_uart:
            card = notecard.OpenSerial(port)
        else:
            card = notecard.OpenI2C(port, 0, 0)
    except Exception as exception:
        raise Exception("error opening notecard: "
                        + NotecardExceptionInfo(exception))

    # If success, do a transaction loop
    print("Performing Transactions...")
    while True:
        time.sleep(2)
        transactionTest(card)


main()
