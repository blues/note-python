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
def config(card):
    """Return the configuration and identity of the satellite (NTN) module: the network it is provisioned for, its modem, its SKU and ordering code, and the firmware it is running.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "ntn.config"}
    return card.Transaction(req)


@validate_card_object
def gps(card, off=None, on=None):
    """On a Notecard paired with a Starnote, this controls whether the Starnote uses a location known to the paired Notecard instead of acquiring one with its own GPS/GNSS module. It does not, by default. On Notecard for Skylo, the satellite radio and the GPS/GNSS are part of the same module. This request controls whether the Notecard uses a known location (typically a fixed location set with `card.location.mode`), instead of acquiring a new location for NTN use.

    Args:
        card (Notecard): The current Notecard object.
        off (bool): When `true`, the Notecard does not supply its location to the NTN module. This is the default configuration.
        on (bool): When `true`, the Notecard supplies its location to the NTN module. If the Notecard does not yet know its location, none is supplied, and this setting has no effect until a location becomes available.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "ntn.gps"}
    if off is not None:
        req["off"] = off
    if on is not None:
        req["on"] = on
    return card.Transaction(req)


@validate_card_object
def reset(card):
    """Once a Notecard is connected to a Starnote device, the presence of a physical Starnote is stored in a permanent configuration that is not affected by a `card.restore` request. This request clears the existing NTN configuration, allowing you to return to testing NTN mode over cellular or WiFi, and enables the Starnote to be paired with a different Notecard device.

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
