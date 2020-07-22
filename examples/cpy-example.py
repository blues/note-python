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
    name = exception.__class__.__name__
    return sys.platform + ": " + name \
        + ": " + ' '.join(map(str, exception.args))


def transactionTest(card):
    req = {"req": "card.status"}
    req["string"] = "string"
    req["bool"] = True
    req["integer"] = 5
    req["real"] = 5.0
    req["object"] = {"temp": 18.6}
    try:
        rsp = card.Transaction(req)
        print(rsp)
    except Exception as exception:
        print("Transaction error: " + NotecardExceptionInfo(exception))
        time.sleep(5)


def main():
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
