"""note-python Circuit Python Sensor example.

This file contains a complete working sample for using the note-python
library with Serial or I2C in Circuit Python to read from a BME680 sensor
and send those values to the Notecard.
"""
import board
import busio
import time
import json
import adafruit_bme680
import notecard

productUID = "com.your-company.your-project"

# Select Serial or I2C with this flag
use_uart = True
card = None

# Configure the Adafruit BME680
i2c = busio.I2C(board.SCL, board.SDA)
bmeSensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Configure the serial connection to the Notecard
if use_uart:
    serial = busio.UART(board.TX, board.RX, baudrate=9600, debug=True)
    card = notecard.OpenSerial(serial)
else:
    card = notecard.OpenI2C(i2c, 0, 0, debug=True)

req = {"req": "hub.set"}
req["product"] = productUID
req["mode"] = "continuous"
card.Transaction(req)

while True:
    temp = bmeSensor.temperature
    humidity = bmeSensor.humidity
    print("\nTemperature: %0.1f C" % temp)
    print("Humidity: %0.1f %%" % humidity)

    req = {"req": "note.add"}
    req["file"] = "sensors.qo"
    req["start"] = True
    req["body"] = {"temp": temp, "humidity": humidity}
    card.Transaction(req)

    time.sleep(15)
