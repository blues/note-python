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
    if files is not None:  # Allow empty list
        req["files"] = files

    response = card.Transaction(req)
    if "err" in response:
        return response

    # Only validate types when fields are present
    if "total" in response and not isinstance(response["total"], int):
        return {"err": "Malformed response: total must be an integer"}
    if "changes" in response and not isinstance(response["changes"], int):
        return {"err": "Malformed response: changes must be an integer"}
    if "info" in response and not isinstance(response["info"], dict):
        return {"err": "Malformed response: info must be a dictionary"}
    return response


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
def stats(card, file=None):
    """Obtain statistics about local notefiles.

    Args:
        card (Notecard): The current Notecard object.
        file (str, optional): Returns stats for the specified Notefile only.

    Returns:
        dict: The result of the Notecard request containing:
            - total (int): Total number of Notes across all Notefiles
            - changes (int): Number of Notes pending sync
            - sync (bool): True if sync is recommended based on pending notes
    """
    req = {"req": "file.stats"}
    if file:
        req["file"] = file
    response = card.Transaction(req)
    if "err" in response:
        return response

    # Only validate types when fields are present
    if "total" in response and not isinstance(response["total"], int):
        return {"err": "Malformed response: total must be an integer"}
    if "changes" in response and not isinstance(response["changes"], int):
        return {"err": "Malformed response: changes must be an integer"}
    if "sync" in response and not isinstance(response["sync"], bool):
        return {"err": "Malformed response: sync must be a boolean"}
    return response


@validate_card_object
def pendingChanges(card):
    """Retrieve information about pending Notehub changes.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "file.changes.pending"}
    response = card.Transaction(req)
    if "err" in response:
        return response

    # Only validate types when fields are present
    if "total" in response and not isinstance(response["total"], int):
        return {"err": "Malformed response: total must be an integer"}
    if "changes" in response and not isinstance(response["changes"], int):
        return {"err": "Malformed response: changes must be an integer"}
    return response
