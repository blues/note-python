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
        dict: The result of the Notecard request containing:
            - changes (int): Notes with pending changes
            - total (int): Total Notes
            - info (dict): Per-file details
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
        dict: The result of the Notecard request. An empty object {} indicates
            success.
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
        file (string, optional): Return stats for the specified Notefile only.

    Returns:
        dict: The result of the Notecard request containing:
            - total (int): Total Notes across all Notefiles
            - changes (int): Notes pending sync
            - sync (bool): True if sync is recommended
    """
    req = {"req": "file.stats"}
    if file:
        req["file"] = file
    return card.Transaction(req)


@validate_card_object
def pendingChanges(card):
    """Retrieve information about pending Notehub changes.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request containing pending changes
            information.
    """
    req = {"req": "file.changes.pending"}

    return card.Transaction(req)
