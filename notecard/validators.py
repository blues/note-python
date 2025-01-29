"""Main Validation decorators for note-python."""

##
# @file validators.py
#
# @brief Validation decorators for note-python.
import sys
import notecard

if sys.implementation.name == "cpython":
    import functools

    def validate_card_object(func):
        """Ensure that the passed-in card is a Notecard."""
        @functools.wraps(func)
        def wrap_validator(*args, **kwargs):
            """Check the instance of the passed-in card."""
            card = args[0]
            if not isinstance(card, notecard.Notecard):
                raise Exception("Notecard object required")

            return func(*args, **kwargs)

        return wrap_validator
else:
    # MicroPython and CircuitPython do not support
    # functools. Do not perform validation for these platforms
    def validate_card_object(func):
        """Skip validation."""
        def wrap_validator(*args, **kwargs):
            """Check the instance of the passed-in card."""
            card = args[0]
            if not isinstance(card, notecard.Notecard):
                raise Exception("Notecard object required")

            return func(*args, **kwargs)

        return wrap_validator


def validate_template_hints(body):
    """Validate type hints in env.template body.

    Args:
        body (dict): Schema with variable names and type hints.

    Raises:
        ValueError: If type hints are invalid.
    """
    if not isinstance(body, dict):
        raise ValueError("Template body must be a dictionary")

    for key, value in body.items():
        if isinstance(value, bool):
            if value is not True:
                raise ValueError(f"Boolean hint for {key} must be True")
        elif isinstance(value, (int, float)):
            valid_types = [
                11, 12, 13, 14, 18,  # signed integers
                21, 22, 23, 24,      # unsigned integers
                12.1, 14.1, 18.1     # floats
            ]
            if value not in valid_types:
                raise ValueError(f"Invalid numeric hint for {key}")
        elif isinstance(value, str):
            try:
                int(value)  # pre v3.2.1 string length
            except ValueError:
                pass  # post v3.2.1 variable length strings
        else:
            raise ValueError(f"Invalid type hint for {key}")
