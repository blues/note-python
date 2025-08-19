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
def changesPending(card):
    """Return info about file changes that are pending upload to Notehub.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.changes.pending"}
    return card.Transaction(req)


@validate_card_object
def changes(card, files=None, tracker=None):
    """Use file.changes request performs queries on a single or multiple files to determine if new Notes are available to read, or if there are unsynced Notes in local Notefiles. Note: This request is a Notefile API request, only. `.qo` Notes in Notehub are automatically ingested and stored, or sent to applicable Routes.

    Args:
        card (Notecard): The current Notecard object.
        files (list): An array of Notefile names to obtain change information from. If not specified, queries all Notefiles.
        tracker (str): An ID string for a change tracker to use to determine changes to Notefiles. Each tracker maintains its own state for monitoring file changes.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.changes"}
    if files:
        req["files"] = files
    if tracker:
        req["tracker"] = tracker
    return card.Transaction(req)


@validate_card_object
def clear(card, file=None):
    """Use to clear the contents of a specified outbound (.qo/.qos) Notefile, deleting all pending Notes.

    Args:
        card (Notecard): The current Notecard object.
        file (str): The name of the Notefile whose Notes you wish to delete.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.clear"}
    if file:
        req["file"] = file
    return card.Transaction(req)


@validate_card_object
def delete(card, files=None):
    """Delete Notefiles and the Notes they contain.

    Args:
        card (Notecard): The current Notecard object.
        files (list): One or more files to delete.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.delete"}
    if files:
        req["files"] = files
    return card.Transaction(req)


@validate_card_object
def stats(card, file=None):
    """Get resource statistics about local Notefiles.

    Args:
        card (Notecard): The current Notecard object.
        file (str): Returns the stats for the specified Notefile only.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.stats"}
    if file:
        req["file"] = file
    return card.Transaction(req)
