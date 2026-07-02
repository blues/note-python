# Notecard Outboard Firmware Update Example

This example demonstrates [Notecard Outboard Firmware Update][odfu], which lets
you update a host MCU's firmware over-the-air from Notehub with no host code
required to perform the download. The Notecard receives the new firmware image
and reprograms the host over the DFU signals on a Notecarrier F.

The [`circuit-python/code.py`](circuit-python/code.py) sample:

1. Configures the Notecard to enable Outboard Firmware Update for the host
   (`card.dfu`, `card.aux`, and `dfu.status`).
2. Blinks the built-in LED with a recognizable pattern. This is the "payload"
   you update over-the-air.

This example targets the [Blues Swan][swan] on a
[Notecarrier F][notecarrier-f]. Cygnet does not support CircuitPython.

## Prerequisites

- A [Blues Swan][swan] running CircuitPython
- A [Notecarrier F][notecarrier-f] with a [Notecard][notecard]
- A [Notehub](https://notehub.io) account and project
- The `notecard` package copied into the `lib/notecard` directory of your
  device (copy the contents of this repo's `notecard/` directory), as described
  in the repo [README](../../README.md)

## Running the example

1. Set the `ProductUID` on your Notecard (via the [in-browser terminal][repl]
   or the [Notecard CLI][cli]) so it reports to your Notehub project, or set
   `productUID` in `code.py`.
2. Copy `circuit-python/code.py` to your Swan (CircuitPython auto-runs `code.py`
   on boot). The LED will blink and the Notecard will report firmware version
   `1.0.0` to Notehub.

## Demonstrating an over-the-air update

1. In `code.py`, change `BLINK_DELAY` (for example to `0.1` for a fast blink)
   and bump `FIRMWARE_VERSION` (for example to `2.0.0`).
2. Build a firmware image and upload it to Notehub, then apply the DFU action
   to the host. See the [Outboard Firmware Update guide][odfu] for the full
   build-and-upload walkthrough.
3. Once the update is applied, the LED blink speed changes and Notehub reports
   the new firmware version — confirming the over-the-air update succeeded.

[odfu]: https://dev.blues.io/notehub/host-firmware-updates/notecard-outboard-firmware-update/
[swan]: https://shop.blues.com/collections/feather-mcu/products/swan
[notecard]: https://shop.blues.io/collections/notecard
[notecarrier-f]: https://shop.blues.io/collections/notecarrier/products/notecarrier-f
[repl]: https://dev.blues.io/terminal/
[cli]: https://dev.blues.io/tools-and-sdks/notecard-cli/
