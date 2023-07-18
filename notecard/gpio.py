"""GPIO abstractions for note-python."""

import sys

if sys.implementation.name == 'circuitpython':
    import digitalio
elif sys.implementation.name == 'micropython':
    import machine
else:
    try:
        with open('/etc/os-release', 'r') as f:
            if 'ID=raspbian' in f.read():
                raspbian = True
                import RPi.GPIO as rpi_gpio
    except IOError:
        pass


class GPIO:
    """GPIO abstraction.

    Supports GPIO on CircuitPython, MicroPython, and Raspbian (Raspberry Pi).
    """

    IN = 0
    OUT = 1
    PULL_UP = 2
    PULL_DOWN = 3
    PULL_NONE = 4

    def direction(self, direction):
        """Set the direction of the pin.

        Does nothing in this base class. Should be implemented by subclasses.
        """
        pass

    def pull(self, pull):
        """Set the pull of the pin.

        Does nothing in this base class. Should be implemented by subclasses.
        """
        pass

    def value(self, value=None):
        """Set the output or get the current level of the pin.

        Does nothing in this base class. Should be implemented by subclasses.
        """
        pass

    @staticmethod
    def setup(pin, direction, pull=None, value=None):
        """Set up a GPIO.

        The platform is detected internally so that the user doesn't need to
        write platform-specific code themselves.
        """
        if sys.implementation.name == 'circuitpython':
            return CircuitPythonGPIO(pin, direction, pull, value)
        elif sys.implementation.name == 'micropython':
            return MicroPythonGPIO(pin, direction, pull, value)
        elif raspbian:
            return RpiGPIO(pin, direction, pull, value)
        else:
            raise NotImplementedError(
                'GPIO not implemented for this platform.')

    def __init__(self, pin, direction, pull=None, value=None):
        """Initialize the GPIO.

        Pin and direction are required arguments. Pull and value will be set
        only if given.
        """
        self.direction(direction)

        if pull is not None:
            self.pull(pull)

        if value is not None:
            self.value(value)


class CircuitPythonGPIO(GPIO):
    """GPIO for CircuitPython."""

    def direction(self, direction):
        """Set the direction of the pin.

        Allowed direction values are GPIO.IN and GPIO.OUT. Other values cause a
        ValueError.
        """
        if direction == GPIO.IN:
            self.pin.direction = digitalio.Direction.INPUT
        elif direction == GPIO.OUT:
            self.pin.direction = digitalio.Direction.OUTPUT
        else:
            raise ValueError(f"Invalid pin direction: {direction}.")

    def pull(self, pull):
        """Set the pull of the pin.

        Allowed pull values are GPIO.PULL_UP, GPIO.PULL_DOWN, and
        GPIO.PULL_NONE. Other values cause a ValueError.
        """
        if pull == GPIO.PULL_UP:
            self.pin.pull = digitalio.Pull.UP
        elif pull == GPIO.PULL_DOWN:
            self.pin.pull = digitalio.Pull.DOWN
        elif pull == GPIO.PULL_NONE:
            self.pin.pull = None
        else:
            raise ValueError(f"Invalid pull value: {pull}.")

    def value(self, value=None):
        """Set the output or get the current level of the pin.

        If value is not given, returns the level of the pin (i.e. the pin is an
        input). If value is given, sets the level of the pin (i.e. the pin is an
        output).
        """
        if value is None:
            return self.pin.value
        else:
            self.pin.value = value

    def __init__(self, pin, direction, pull=None, value=None):
        """Initialize the GPIO.

        Pin and direction are required arguments. Pull and value will be set
        only if given.
        """
        self.pin = digitalio.DigitalInOut(pin)
        super().__init__(pin, direction, pull, value)


class MicroPythonGPIO(GPIO):
    """GPIO for MicroPython."""

    def direction(self, direction):
        """Set the direction of the pin.

        Allowed direction values are GPIO.IN and GPIO.OUT. Other values cause a
        ValueError.
        """
        if direction == GPIO.IN:
            self.pin.init(mode=machine.Pin.IN)
        elif direction == GPIO.OUT:
            self.pin.init(mode=machine.Pin.OUT)
        else:
            raise ValueError(f"Invalid pin direction: {direction}.")

    def pull(self, pull):
        """Set the pull of the pin.

        Allowed pull values are GPIO.PULL_UP, GPIO.PULL_DOWN, and
        GPIO.PULL_NONE. Other values cause a ValueError.
        """
        if pull == GPIO.PULL_UP:
            self.pin.init(pull=machine.Pin.PULL_UP)
        elif pull == GPIO.PULL_DOWN:
            self.pin.init(pull=machine.Pin.PULL_DOWN)
        elif pull == GPIO.PULL_NONE:
            self.pin.init(pull=None)
        else:
            raise ValueError(f"Invalid pull value: {pull}.")

    def value(self, value=None):
        """Set the output or get the current level of the pin.

        If value is not given, returns the level of the pin (i.e. the pin is an
        input). If value is given, sets the level of the pin (i.e. the pin is an
        output).
        """
        if value is None:
            return self.pin.value()
        else:
            self.pin.init(value=value)

    def __init__(self, pin, direction, pull=None, value=None):
        """Initialize the GPIO.

        Pin and direction are required arguments. Pull and value will be set
        only if given.
        """
        self.pin = machine.Pin(pin)
        super().__init__(pin, direction, pull, value)


class RpiGPIO(GPIO):
    """GPIO for Raspbian (Raspberry Pi)."""

    def direction(self, direction):
        """Set the direction of the pin.

        Allowed direction values are GPIO.IN and GPIO.OUT. Other values cause a
        ValueError.
        """
        if direction == GPIO.IN:
            self.rpi_direction = rpi_gpio.IN
            rpi_gpio.setup(self.pin, direction=rpi_gpio.IN)
        elif direction == GPIO.OUT:
            self.rpi_direction = rpi_gpio.OUT
            rpi_gpio.setup(self.pin, direction=rpi_gpio.OUT)
        else:
            raise ValueError(f"Invalid pin direction: {direction}.")

    def pull(self, pull):
        """Set the pull of the pin.

        Allowed pull values are GPIO.PULL_UP, GPIO.PULL_DOWN, and
        GPIO.PULL_NONE. Other values cause a ValueError.
        """
        if pull == GPIO.PULL_UP:
            rpi_gpio.setup(self.pin,
                           direction=self.rpi_direction,
                           pull_up_down=rpi_gpio.PUD_UP)
        elif pull == GPIO.PULL_DOWN:
            rpi_gpio.setup(self.pin,
                           direction=self.rpi_direction,
                           pull_up_down=GPIO.PUD_DOWN)
        elif pull == GPIO.PULL_NONE:
            rpi_gpio.setup(self.pin,
                           direction=self.rpi_direction,
                           pull_up_down=rpi_gpio.PUD_OFF)
        else:
            raise ValueError(f"Invalid pull value: {pull}.")

    def value(self, value=None):
        """Set the output or get the current level of the pin.

        If value is not given, returns the level of the pin (i.e. the pin is an
        input). If value is given, sets the level of the pin (i.e. the pin is an
        output).
        """
        if value is None:
            return rpi_gpio.input(self.pin)
        else:
            rpi_gpio.output(self.pin, value)

    def __init__(self, pin, direction, pull=None, value=None):
        """Initialize the GPIO.

        Pin and direction are required arguments. Pull and value will be set
        only if given.
        """
        self.pin = pin
        super().__init__(pin, direction, pull, value)
