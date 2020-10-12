"""Main Validation decorators for note-python."""

##
# @file validators.py
#
# @brief Validation decorators for note-python.
import functools
import notecard


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
