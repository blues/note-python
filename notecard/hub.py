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
from notecard.validators import validate_card_object


@validate_card_object
def set(card, product=None, sn=None, mode=None, outbound=None,
        inbound=None, duration=None, sync=False, align=None, voutbound=None,
        vinbound=None, host=None):
    """Configure Notehub behavior on the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        product (string): The ProductUID of the project.
        sn (string): The Serial Number of the device.
        mode (string): The sync mode to use.
        outbound (int): Max time to wait to sync outgoing data.
        inbound (int): Max time to wait to sync incoming data.
        duration (int): If in continuous mode, the amount of time, in minutes,
            of each session.
        sync (bool): If in continuous mode, whether to automatically
            sync each time a change is detected on the device or Notehub.
        align (bool): To align syncs to a regular time-interval, as opposed
            to using max time values.
        voutbound (string): Overrides "outbound" with a voltage-variable value.
        vinbound (string): Overrides "inbound" with a voltage-variable value.
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
    if outbound:
        req["outbound"] = outbound
    if inbound:
        req["inbound"] = inbound
    if duration:
        req["duration"] = duration
    if sync is not None:
        req["sync"] = sync
    if align is not None:
        req["align"] = align
    if voutbound:
        req["voutbound"] = voutbound
    if vinbound:
        req["vinbound"] = vinbound
    if host:
        req["host"] = host

    return card.Transaction(req)


@validate_card_object
def sync(card, allow=None):
    """Initiate a sync of the Notecard to Notehub.

    Args:
        card (Notecard): The current Notecard object.
        allow (bool): When True, allows syncing over a non-terrestrial
            network even if the Notefile is not in compact mode.

    Returns:
        dict: The result of the Notecard request containing sync status.
    """
    req = {"req": "hub.sync"}
    if allow is not None:
        req["allow"] = allow
    return card.Transaction(req)


@validate_card_object
def syncStatus(card, sync=None, ntn=None):
    """Retrieve the status of a sync request.

    Args:
        card (Notecard): The current Notecard object.
        sync (bool): True if sync should be auto-initiated pending
            outbound data.
        ntn (bool): When True, returns additional status information about
            non-terrestrial network sync status.

    Returns:
        dict: The result of the Notecard request containing sync status,
        including NTN details when requested.
    """
    req = {"req": "hub.sync.status"}
    if sync is not None:
        req["sync"] = sync
    if ntn is not None:
        req["ntn"] = ntn

    return card.Transaction(req)


@validate_card_object
def status(card, ntn=None):
    """Retrieve the status of the Notecard's connection.

    Args:
        card (Notecard): The current Notecard object.
        ntn (bool): When True, returns additional status information about
            non-terrestrial network connectivity.

    Returns:
        dict: The result of the Notecard request containing connection status,
        including NTN details when requested.
    """
    req = {"req": "hub.status"}
    if ntn is not None:
        req["ntn"] = ntn
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
    """Retrieve the current Notehub configuration parameters.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "hub.get"}
    return card.Transaction(req)
