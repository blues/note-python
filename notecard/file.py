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
    if files is not None:  # Allow empty list
        req["files"] = files

    response = card.Transaction(req)
    if "err" in response:
        return response
    # Check for required fields first
    if not all(key in response for key in ['total', 'changes', 'info']):
        return {"err": "Missing required fields in response"}
    # Then validate field types
    if not isinstance(response['total'], int):
        return {"err": "Malformed response: total must be an integer"}
    if not isinstance(response['changes'], int):
        return {"err": "Malformed response: changes must be an integer"}
    if not isinstance(response['info'], dict):
        return {"err": "Malformed response: info must be a dictionary"}
    return response


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
    response = card.Transaction(req)
    return response


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
    response = card.Transaction(req)
    if "err" in response:
        return response
    # Check for required fields
    if not all(key in response for key in ['total', 'changes', 'sync']):
        return {"err": "Missing required fields in response"}
    # Validate field types
    if not isinstance(response['total'], int):
        return {"err": "Malformed response: total must be an integer"}
    if not isinstance(response['changes'], int):
        return {"err": "Malformed response: changes must be an integer"}
    if not isinstance(response['sync'], bool):
        return {"err": "Malformed response: sync must be a boolean"}
    return response


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
    response = card.Transaction(req)
    if "err" in response:
        return response
    # Validate response format - should contain total and changes
    if not all(key in response for key in ['total', 'changes']):
        return {"err": "Missing required fields in response"}
    # Validate field types
    if not isinstance(response.get('total'), int):
        return {"err": "Malformed response: total must be an integer"}
    if not isinstance(response.get('changes'), int):
        return {"err": "Malformed response: changes must be an integer"}
    return response
