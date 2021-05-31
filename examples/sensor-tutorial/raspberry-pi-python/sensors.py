"""note-python Python Sensor example.

This file contains a complete working sample for using the note-python
library with Serial or I2C in Python to read from a BME680 sensor
and send those values to the Notecard.
"""
import json
import notecard
from periphery import I2C, Serial
import time
import bme680

bme_sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

bme_sensor.set_humidity_oversample(bme680.OS_2X)
bme_sensor.set_temperature_oversample(bme680.OS_8X)

bme_sensor.get_sensor_data()

productUID = "com.[your-company].[your-product]"

# Select Serial or I2C with this flag
use_uart = True
card = None

# Configure the serial connection to the Notecard
if use_uart:
    serial = Serial('/dev/ttyS0', 9600)
    card = notecard.OpenSerial(serial, debug=True)
else:
    port = I2C("/dev/i2c-1")
    card = notecard.OpenI2C(port, 0, 0, debug=True)


req = {"req": "hub.set"}
req["product"] = productUID
req["mode"] = "continuous"
card.Transaction(req)

while True:
    bme_sensor.get_sensor_data()

    temp = bme_sensor.data.temperature
    humidity = bme_sensor.data.humidity

    print('Temperature: {} degrees C'.format(temp))
    print('Humidity: {}%'.format(humidity))

    req = {"req": "note.add"}
    req["file"] = "sensors.qo"
    req["start"] = True
    req["body"] = {"temp": temp, "humidity": humidity}
    card.Transaction(req)

    time.sleep(15)
