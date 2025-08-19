"""ntn Fluent API Helper."""

##
# @file ntn.py
#
# @brief ntn Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling ntn.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def gps(card, on=None, off=None):
    """Determine whether a Notecard should override a paired Starnote's GPS/GNSS location with its own GPS/GNSS location. The paired Starnote uses its own GPS/GNSS location by default.

    Args:
        card (Notecard): The current Notecard object.
        on (bool): When `true`, a Starnote will use the GPS/GNSS location from its paired Notecard, instead of its own GPS/GNSS location.
        off (bool): When `true`, a paired Starnote will use its own GPS/GNSS location. This is the default configuration.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "ntn.gps"}
    if on is not None:
        req["on"] = on
    if off is not None:
        req["off"] = off
    return card.Transaction(req)


@validate_card_object
def reset(card):
    """Once a Notecard is connected to a Starnote device, the presence of a physical Starnote is stored in a permanent configuration that is not affected by a `card.restore` request. This request clears this configuration and allows you to return to testing NTN mode over cellular or Wi-Fi.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "ntn.reset"}
    return card.Transaction(req)


@validate_card_object
def status(card):
    """Display the current status of a Notecard's connection to a paired Starnote.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "ntn.status"}
    return card.Transaction(req)
