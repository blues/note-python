import sys
import os
import time

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402

# For UART and I2C IO
use_periphery = False
if sys.implementation.name != 'cpython':
    raise Exception("Please run this example in a CPython environment.")

if sys.platform == "linux" or sys.platform == "linux2":
    use_periphery = True
    from periphery import Serial  # noqa: E402
else:
    import serial  # noqa: E402


def NotecardExceptionInfo(exception):
    s1 = '{}'.format(sys.exc_info()[-1].tb_lineno)
    s2 = exception.__class__.__name__
    return "line " + s1 + ": " + s2 + ": " + ' '.join(map(str, exception.args))


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
        if sys.platform == "linux" or sys.platform == "linux2":
            if use_periphery:
                port = Serial("/dev/serial0", 9600)
            else:
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

    # If success, do a transaction loop
    print("Performing Transactions...")
    while True:
        time.sleep(2)
        transactionTest(card)


main()
