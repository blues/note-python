"""file Fluent API Helper."""

##
# @file file.py
#
# @brief file Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling file.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def changes(card, tracker=None, files=None):
    """Perform individual or batch queries on Notefiles.

    Args:
        card (Notecard): The current Notecard object.
        tracker (string): A developer-defined tracker ID.
        files (array): A list of Notefiles to retrieve changes for.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "file.changes"}
    if tracker:
        req["tracker"] = tracker
    if files:
        req["files"] = files
    return card.Transaction(req)


@validate_card_object
def delete(card, files=None):
    """Delete individual notefiles and their contents.

    Args:
        card (Notecard): The current Notecard object.
        files (array): A list of Notefiles to delete.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "file.delete"}
    if files:
        req["files"] = files
    return card.Transaction(req)


@validate_card_object
def stats(card, usage=None):
    """Obtain statistics about local notefiles.

    Args:
        card (Notecard): The current Notecard object.
        usage (str, optional): When 'true', include detailed resource usage
            stats.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.stats"}
    if usage:
        req["usage"] = usage
    return card.Transaction(req)


@validate_card_object
def pendingChanges(card):
    """Retrieve information about pending Notehub changes.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.changes.pending"}
    return card.Transaction(req)


@validate_card_object
def monitor(card, files=None, usage=None):
    """Monitor one or more files in detail, including resource usage stats.

    Args:
        card (Notecard): The current Notecard object.
        files (list, optional): List of Notefiles to monitor. Defaults to None.
        usage (str, optional): When 'true', include detailed resource usage
            stats.

    Returns:
        dict: Detailed information about each file, including usage metrics.
    """
    req = {"req": "file.monitor"}
    if files is not None:
        req["files"] = files
    if usage:
        req["usage"] = usage
    return card.Transaction(req)


@validate_card_object
def track(card, files=None, interval=None, duration=None):
    """Enable continuous tracking of file changes.

    Args:
        card (Notecard): The current Notecard object.
        files (list, optional): List of Notefiles to track. Defaults to None.
        interval (int, optional): Polling interval in seconds. Defaults to
            None.
        duration (int, optional): Total tracking duration in seconds. Defaults
            to None.

    Returns:
        dict: The result of the Notecard request with tracking configuration.
    """
    req = {"req": "file.track"}
    if files:
        req["files"] = files
    if interval is not None:
        req["interval"] = interval
    if duration is not None:
        req["duration"] = duration
    return card.Transaction(req)
