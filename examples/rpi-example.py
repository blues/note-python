"""note-python Raspberry Pi example.

This file contains a complete working sample for using the note-python
library on a Raspberry Pi device.
"""
import sys
import os
import time

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard   # noqa: E402

# Choose either UART or I2C for Notecard
use_uart = True

if sys.implementation.name != 'cpython':
    raise Exception("Please run this example in a \
                    Raspberry Pi or CPython environment.")

from periphery import I2C  # noqa: E402
from periphery import Serial  # noqa: E402


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
            port = Serial("/dev/serial0", 9600)
        else:
            port = I2C("/dev/i2c-1")
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
