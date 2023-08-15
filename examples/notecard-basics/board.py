"""
Define peripherals for different types of boards.

This module, or it's variants are  used by the mpy_example to use the appropriate
UART or I2C configuration for the particular board being used.
The values here are defaults. The definitions for real boards are located in ./mpy_board/*
at the root of the repo.
"""


"""
The UART instance to use that is connected to Notecard.
"""
UART = 2

"""
The I2C ID and SDL and SDA pins of the I2C bus connected to Notecard
"""
I2C_ID = 0
SCL = 0
SDA = 0
