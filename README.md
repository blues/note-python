# note-python

Python library for communicating with the Blues Wireless Notecard over serial or I²C.

![Build](https://github.com/blues/note-python/workflows/Python%20package/badge.svg)

This library allows you to control a Notecard by coding in Python and works in a desktop setting, on Single-Board Computers like the Raspberry Pi, and on Microcontrollers with MicroPython or CircuitPython support.

## Installation

With pi-py:

```bash
pip install note-python
```

For use with MicroPython or CircuitPython, copy the contents of the `notecard` directory into the `lib` directory of your device.

## Usage

```python
import notecard
```

The `note-python` library requires a pointer to a serial or i2c object that you initialize and pass into the library. This object differs based on platform, so consult the [examples](examples/) directory for platform-specific guidance.

### Serial Configuration

```python
# Use python-periphery on a desktop or Raspberry Pi 
from periphery import Serial
port = Serial("/dev/serial0", 9600)

card = notecard.OpenSerial(port)
```

### I2C Confgiguration

```python
# Use python-periphery on a desktop or Raspberry Pi 
from periphery import Serial
port = I2C("/dev/i2c-1")
card = notecard.OpenI2C(port, 0, 0)
```

### Sending Notecard Requests

Whether using Serial or I2C, sending Notecard requests and reading responses follows the same pattern:

1. Create a JSON object that adheres to the Notecard API
2. Call `card.Transaction`, `card.Request` or `card.RequestResponse` and pass in the request JSON object.
3. Make sure the response contains the data you need

```python
# Construct a JSON Object to add a Note to the Notecard
req = {"req": "note.add"}
req["body"] = {"temp": 18.6}

rsp = card.Transaction(req)
print(rsp) # {"total":1}
```

### Using the Library Fluent API

The `notecard` class allows complete access to the Notecard API via manual JSON object construction and the `Transaction`, `Request`, and `RequestResponse` methods. Alternatively, you can import one or more Fluent API helpers to work with common aspects of the Notecard API without having to author JSON objects, by hand. **Note** that not all aspects of the Notecard API are available using these helpers. For a complete list of supported helpers, visit the [API](API.md) doc.

Here's an example that uses the `hub` helper to set the Notecard Product UID in CircuitPython:

```python
import board
import busio

import notecard
from notecard import card, hub, note

port = busio.I2C(board.SCL, board.SDA)
nCard = notecard.OpenI2C(port, 0, 0, debug=True)

productUID  = "com.blues.brandon.tester"
rsp = hub.set(nCard, productUID, mode="continuous", sync=True)

print(rsp) # {}
```

## Documentation

The documentation for this library can be found at the Blues Wireless [wireless.dev](https//wireless.dev/reference/note-python) site.

## Examples

The [examples](examples/) directory contains examples for using this library with:

- [Serial](examples/serial-example.py)
- [I2C](examples/i2c-example.py)
- [RaspberryPi](examples/rpi-example.py)
- [CircuitPython](examples/cpy-example.py)
- [MicroPython](examples/mpy-example.py)

## Contributing

We love issues, fixes, and pull requests from everyone. By participating in this project, you agree to abide by the Blues Inc [code of conduct].

For details on contributions we accept and the process for contributing, see our [contribution guide](CONTRIBUTING.md)

## Running the Tests

If you're planning to contribute to this repo, please be sure to run the tests before submitting a PR. First run:

```bash
pip install -r requirements.txt
```

Then, run the linter and tests using the included `MAKEFILE`.

```bash
make -f MAKEFILE
```

Alternatively, you can inspect the contents of the [MAKEFILE](MAKEFILE) and run `flake8` and `pytest` directly. Be aware, however, that the commands in the `MAKEFILE` run against every pull request, so your best bet is to ensure these tests are successful before submitting your PR.

## More Information

For additional Notecard SDKs and Libraries, see:

* [note-c](note-c) for Standard C support
* [note-go](note-go) for Go
* [note-arduino](note-arduino) for Arduino 

## To learn more about Blues Wireless, the Notecard and Notehub, see:

* [blues.com](https://blues.com)
* [notehub.io][Notehub]
* [wireless.dev](https://wireless.dev)

## License

Copyright (c) 2019 Blues Inc. Released under the MIT license. See [LICENSE](LICENSE) for details.

[code of conduct]: https://blues.github.io/opensource/code-of-conduct
[Notehub]: https://notehub.io