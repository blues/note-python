
import sys

# Choose either UART or I2C for Notecard
use_uart = True

# For UART and I2C IO
use_periphery = False
if sys.implementation.name == 'circuitpython':
    import board
    import busio
elif sys.implementation.name == 'micropython':
    from machine import UART
    from machine import I2C
elif sys.implementation.name == 'cpython':
    if sys.platform == "linux" or sys.platform == "linux2":
        use_periphery = True
        from periphery import I2C
        from periphery import Serial
    else:
        import serial
else:
    raise Exception("Unsupported platform: " + sys.platform)

# General imports
import time
import notecard

# Main loop
def main():

    # Initialize
    print("opening port")
    try:
        if sys.implementation.name == 'circuitpython':
            if use_uart:
                # https://circuitpython.readthedocs.io/en/2.x/shared-bindings/busio/UART.html
                port = busio.UART(board.TX, board.RX, baudrate=9600)
            else:
                # https://circuitpython.readthedocs.io/en/2.x/shared-bindings/busio/I2C.html
                port = busio.I2C(board.SCL, board.SDA)
        elif sys.implementation.name == 'micropython':
            if use_uart:
                # https://docs.micropython.org/en/latest/library/machine.UART.html
                # ESP32 IO2 RX:16 TX:17
                port = UART(2, 9600)
                port.init(9600, bits=8, parity=None, stop=1)
            else:
                # https://docs.micropython.org/en/latest/library/machine.I2C.html
                port = I2C()
        elif sys.implementation.name == 'cpython':
            if use_uart:
                # https://github.com/vsergeev/python-periphery#serial
                if sys.platform == "linux" or sys.platform == "linux2":
                    if use_periphery:
                        port = Serial("/dev/serial0", 9600)
                    else:
                        port = serial.Serial(port="/dev/serial0", baudrate=9600)
                elif sys.platform == "darwin":
                    port = serial.Serial(port="/dev/tty.usbmodemNote11", baudrate=9600)
                elif sys.platform == "win32":
                    port = serial.Serial(port="COM21", baudrate=9600)
            else:
                # https://github.com/vsergeev/python-periphery#i2c
                if use_periphery:
                    port = I2C("/dev/i2c-1")
                else:
                    raise Exception("I2C not supported on platform: " + sys.platform)
    except Exception as exception:
        raise Exception("error opening port: " + ExceptionInfo(exception))

    print("opening notecard")
    try:
        if use_uart:
            card = notecard.OpenSerial(port)
        else:
            card = notecard.OpenI2C(port, 0, 0)
    except Exception as exception:
        raise Exception("error opening notecard: " + ExceptionInfo(exception))
    
    # If success, do a transaction loop
    print("transaction loop")
    while True:
        time.sleep(2)
        transactionTest(card)

# Test the Notecard with a single transaction
def transactionTest(card):
    req = {"req":"card.status"}
    req["string"] = "string"
    req["bool"] = True
    req["integer"] = 5
    req["real"] = 5.0
    req["object"] = {"temp":18.6}
    try:
        rsp = card.Transaction(req)
        print(rsp)
    except Exception as exception:
        print("transaction error: " + ExceptionInfo(exception))
        time.sleep(5)
        
# Format an exception string
def ExceptionInfo(exception):
    s1 = '{}'.format(sys.exc_info()[-1].tb_lineno)
    s2 = exception.__class__.__name__
    return "line " + s1 +  ": " + s2 + ": " + ' '.join(map(str,exception.args))
    

# Invoke Main here so that we don't need to be strict about defining functions before use
main()
