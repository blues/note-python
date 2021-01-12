"""note-python CircuitPython example.

This file contains a complete working sample for using the note-python
library on a CircuitPython device.
"""
import sys
import time
import notecard

# Choose either UART or I2C for Notecard
use_uart = True

if sys.implementation.name != 'circuitpython':
    raise Exception("Please run this example in a CircuitPython environment.")

import board  # noqa: E402
import busio  # noqa: E402


def NotecardExceptionInfo(exception):
    """Construct a formatted Exception string.

    Args:
        exception (Exception): An exception object.

    Returns:
        string: a summary of the exception with line number and details.
    """
    name = exception.__class__.__name__
    return sys.platform + ": " + name \
        + ": " + ' '.join(map(str, exception.args))


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
            port = busio.UART(board.TX, board.RX, baudrate=9600)
        else:
            port = busio.I2C(board.SCL, board.SDA)
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
