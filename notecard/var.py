"""var Fluent API Helper."""

##
# @file var.py
#
# @brief var Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling var.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def delete(card, file=None, name=None):
    """Delete a Note from a DB Notefile by its `name`. Provides a simpler interface to the note.delete API.

    Args:
        card (Notecard): The current Notecard object.
        file (str): The name of the DB Notefile that contains the Note to delete. Default value is `vars.db`.
        name (str): The unique Note ID.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "var.delete"}
    if file:
        req["file"] = file
    if name:
        req["name"] = name
    return card.Transaction(req)


@validate_card_object
def get(card, file=None, name=None):
    """Retrieve a Note from a DB Notefile. Provides a simpler interface to the note.get API.

    Args:
        card (Notecard): The current Notecard object.
        file (str): The name of the DB Notefile that contains the Note to retrieve. Default value is `vars.db`.
        name (str): The unique Note ID.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "var.get"}
    if file:
        req["file"] = file
    if name:
        req["name"] = name
    return card.Transaction(req)


@validate_card_object
def set(card, file=None, flag=None, name=None, sync=None, text=None, value=None):
    """Add or updates a Note in a DB Notefile, replacing the existing body with the specified key-value pair where text, value, or flag is the key. Provides a simpler interface to the note.update API.

    Args:
        card (Notecard): The current Notecard object.
        file (str): The name of the DB Notefile that contains the Note to add or update. Default value is `vars.db`.
        flag (bool): The boolean value to be stored in the DB Notefile.
        name (str): The unique Note ID.
        sync (bool): Set to `true` to immediately sync any changes.
        text (str): The string-based value to be stored in the DB Notefile.
        value (int): The numeric value to be stored in the DB Notefile.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "var.set"}
    if file:
        req["file"] = file
    if flag is not None:
        req["flag"] = flag
    if name:
        req["name"] = name
    if sync is not None:
        req["sync"] = sync
    if text:
        req["text"] = text
    if value is not None:
        req["value"] = value
    return card.Transaction(req)
