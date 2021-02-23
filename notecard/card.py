"""card Fluent API Helper."""

##
# @file card.py
#
# @brief card Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling card.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

import notecard
import sys
if sys.implementation.name == 'micropython':
    from validators import validate_card_object
else:
    from .validators import validate_card_object


@validate_card_object
def attn(card, mode=None, files=None, seconds=None, payload=None, start=None):
    """Configure interrupt detection between a host and Notecard.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The attn mode to set.
        files (array): A collection of notefiles to watch.
        seconds (int): A timeout to use when arming attn mode.
        payload (int): When using sleep mode, a payload of data from the host
            that the Notecard should hold in memory until retrieved by
            the host.
        start (bool): When using sleep mode and the host has reawakened,
            request the Notecard to return the stored payload.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.attn"}
    if mode:
        req["mode"] = mode
    if files:
        req["files"] = files
    if seconds:
        req["seconds"] = seconds
    if payload:
        req["payload"] = payload
    if start:
        req["start"] = start
    return card.Transaction(req)


@validate_card_object
def time(card):
    """Retrieve the current time and date from the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.time"}
    return card.Transaction(req)


@validate_card_object
def status(card):
    """Retrieve the status of the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.status"}
    return card.Transaction(req)


@validate_card_object
def temp(card, minutes=None):
    """Retrieve the current temperature from the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): If specified, creates a templated _temp.qo file that
            gathers Notecard temperature value at the specified interval.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.temp"}
    if minutes:
        req["minutes"] = minutes
    return card.Transaction(req)


@validate_card_object
def version(card):
    """Retrieve firmware version information from the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.version"}
    return card.Transaction(req)


@validate_card_object
def voltage(card, hours=None, offset=None, vmax=None, vmin=None):
    """Retrieve current and historical voltage info from the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        hours (int): Number of hours to analyze.
        offset (int): Number of hours to offset.
        vmax (decimal): max voltage level to report.
        vmin (decimal): min voltage level to report.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.voltage"}
    if hours:
        req["hours"] = hours
    if offset:
        req["offset"] = offset
    if vmax:
        req["vmax"] = vmax
    if vmin:
        req["vmin"] = vmin
    return card.Transaction(req)


@validate_card_object
def wireless(card, mode=None, apn=None):
    """Retrieve wireless modem info or customize modem behavior.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The wireless module mode to set.
        apn (string): Access Point Name (APN) when using an external SIM.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.wireless"}
    if mode:
        req["mode"] = mode
    if apn:
        req["apn"] = apn

    return card.Transaction(req)
