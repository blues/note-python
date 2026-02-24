"""Simple MicroPython script to validate Notestation dev environment.

Assumes Notestation provides a UART connection at UART2 or adjust accordingly.
"""

from machine import UART
import notecard

port = UART(2, 9600)
port.init(9600, bits=8, parity=None, stop=1)

card = notecard.OpenSerial(port)

rsp = card.Transaction({"req": "card.version"})
print(rsp)