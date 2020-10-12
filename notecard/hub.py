"""hub Fluent API Helper."""

##
# @file hub.py
#
# @brief hub Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling hub.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

import notecard
from .validators import validate_card_object


@validate_card_object
def set(card, product, sn=None, mode=None, minutes=None,
        hours=None, sync=False, align=None, vminutes=None,
        vhours=None, host=None):
    """Configure Notehub behavior on the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        product (string): The ProductUID of the project.
        sn (string): The Serial Number of the device.
        mode (string): The sync mode to use.
        minutes (int): Max time to wait to sync outgoing data.
        hours (int): Max time to wait to sync incoming data.
        sync (bool): If in continuous mode, whether to automatically
            sync each time a change is detected on the device or Notehub.
        align (bool): To align syncs to a regular time-interval, as opposed
            to using max time values.
        vminutes (string): Overrides "minutes" with a voltage-variable value.
        vhours (string): Overrides "hours" with a voltage-variable value.
        host (string): URL of an alternative or private Notehub instance.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.set"}
    if product:
        req["product"] = product
    if sn:
        req["sn"] = sn
    if mode:
        req["mode"] = mode
    if minutes:
        req["minutes"] = minutes
    if hours:
        req["hours"] = hours
    if sync is not None:
        req["sync"] = sync
    if align is not None:
        req["align"] = align
    if vminutes:
        req["vminutes"] = vminutes
    if vhours:
        req["vhours"] = vhours
    if host:
        req["host"] = host

    return card.Transaction(req)


@validate_card_object
def sync(card):
    """Initiate a sync of the Notecard to Notehub.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.sync"}
    return card.Transaction(req)


@validate_card_object
def syncStatus(card, sync=None):
    """Retrive the status of a sync request.

    Args:
        card (Notecard): The current Notecard object.
        sync (bool): True if sync should be auto-initiated pending
            outbound data.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.sync.status"}
    if sync is not None:
        req["sync"] = sync

    return card.Transaction(req)


@validate_card_object
def status(card):
    """Retrieve the status of the Notecard's connection.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.status"}
    return card.Transaction(req)


@validate_card_object
def log(card, text, alert=False, sync=False):
    """Send a log request to the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        text (string): The ProductUID of the project.
        alert (bool): True if the message is urgent.
        sync (bool): Whether to sync right away.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.log"}
    req["text"] = text
    req["alert"] = alert
    req["sync"] = sync
    return card.Transaction(req)


@validate_card_object
def get(card):
    """Retrive the current Notehub configuration parameters.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.get"}
    return card.Transaction(req)
