"""note-python CircuitPython Outboard Firmware Update example.

This file contains a complete working sample for demonstrating Notecard
Outboard Firmware Update from CircuitPython. It configures the Notecard to
enable Outboard Firmware Update for the host, then blinks the built-in LED with
a recognizable pattern that serves as the "payload" you update over-the-air.

To demonstrate an update: change BLINK_DELAY (and bump FIRMWARE_VERSION) below,
build a new firmware image, upload it to Notehub, and apply the DFU action to
the host. The blink speed (and reported version) will change once the update
is applied.

This example targets the Blues Swan on a Notecarrier F. Cygnet does not support
CircuitPython.
"""
import time
import board
import digitalio
import notecard
from notecard import card as card_helper
from notecard import dfu as dfu_helper
from notecard import hub as hub_helper

# The unique Product Identifier for your device. Claim one in a Notehub project.
productUID = "com.your-company.your-project"

# The firmware version reported to Notehub via dfu.status. Bump this (and change
# BLINK_DELAY) when you build a new image to update to.
FIRMWARE_VERSION = "1.0.0"

# Seconds the LED stays on/off. Change this to make the update visually obvious.
BLINK_DELAY = 0.5


def configure_outboard_dfu(card):
    """Put the Notecard online and enable Outboard Firmware Update for the host.

    Outboard Firmware Update requires the Notecard to be in "continuous" or
    "periodic" mode. On a Notecarrier F the DFU signals are routed over the
    Notecard's shared AUX pins, so card.dfu uses mode "aux" and card.aux is set
    to "off" to free those pins for DFU.
    """
    hub_helper.set(card, product=productUID, mode="continuous",
                   sn="circuitpython-notecard")

    # Enable Outboard Firmware Update and tell the Notecard the host MCU type.
    card_helper.dfu(card, name="stm32", on=True, mode="aux")

    # Free the AUX pins so they can be used for Outboard Firmware Update.
    card_helper.aux(card, mode="off")

    # Enable host DFU and report the running firmware version to Notehub.
    dfu_helper.status(card, on=True, version=FIRMWARE_VERSION)


def main():
    """Enable Outboard DFU, then blink the built-in LED as the update payload."""
    i2c = board.I2C()
    card = notecard.OpenI2C(i2c, 0, 0, debug=True)

    configure_outboard_dfu(card)

    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

    print("Running firmware version {}. Hit CTRL-C to stop.".format(FIRMWARE_VERSION))
    while True:
        led.value = True
        time.sleep(BLINK_DELAY)
        led.value = False
        time.sleep(BLINK_DELAY)


main()
