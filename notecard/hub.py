"""hub Fluent API Helper.

This module contains helper methods for calling hub.*
Notecard API commands.
"""
import notecard
from .validators import validate_card_object


@validate_card_object
def set(card, product, sn=None,
        mode=None, minutes=None, hours=None, sync=False):
    """Configure Notehub behavior on the Notecard.

    Args:
        product (string): The ProductUID of the project.
        sn (string): The Serial Number of the device.
        mode (string): The sync mode to use.
        minutes (int): Max time to wait to sync outgoing data.
        hours (int): Max time to wait to sync incoming data.
        sync (bool): If in continuous mode, whether to automatically
            sync each time a change is detected on the device or Notehub.

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
    if sync:
        req["sync"] = True

    return card.Transaction(req)


@validate_card_object
def sync(card):
    """Initiate a sync of the Notecard to Notehub.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.sync"}
    return card.Transaction(req)


@validate_card_object
def syncStatus(card):
    """Retrive the status of a sync request.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.sync.status"}
    return card.Transaction(req)


@validate_card_object
def status(card):
    """Retrieve the status of the Notecard's connection.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.status"}
    return card.Transaction(req)


@validate_card_object
def log(card, text, sync=False):
    """Send a log request to the Notecard.

    Args:
        text (string): The ProductUID of the project.
        sync (bool): Whether to sync right away.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.log"}
    req["text"] = text
    req["sync"] = sync
    return card.Transaction(req)


@validate_card_object
def get(card):
    """Retrive the current Notehub configuration parameters.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.get"}
    return card.Transaction(req)
