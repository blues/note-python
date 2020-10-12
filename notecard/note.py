"""note Fluent API Helper."""

##
# @file note.py
#
# @brief note Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling note.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

import notecard
from .validators import validate_card_object


@validate_card_object
def changes(card, file=None, tracker=None, maximum=None,
            start=None, stop=None, deleted=None, delete=None):
    """Incrementally retrieve changes within a Notefile.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The name of the file.
        tracker (string): A developer-defined tracker ID.
        maximum (int): Maximum number of notes to return.
        start (bool): Should tracker be reset to the beginning
            before a get.
        stop (bool): Should tracker be deleted after get.
        deleted (bool): Should deleted notes be returned.
        delete (bool): Should notes in a response be auto-deleted.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "note.changes"}
    if file:
        req["file"] = file
    if tracker:
        req["tracker"] = tracker
    if maximum:
        req["max"] = maximum
    if start is not None:
        req["start"] = start
    if stop is not None:
        req["stop"] = stop
    if deleted is not None:
        req["deleted"] = deleted
    if delete is not None:
        req["delete"] = delete
    return card.Transaction(req)


@validate_card_object
def get(card, file="data.qi", note_id=None, delete=None, deleted=None):
    """Retrive a note from an inbound or DB Notefile.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The inbound or DB notefile to retrive a
            Notefile from.
        note_id (string): (DB files only) The ID of the note to retrive.
        delete (bool): Whether to delete the note after retrieval.
        deleted (bool): Whether to allow retrival of a deleted note.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "note.get"}
    req["file"] = file
    if note_id:
        req["note"] = note_id
    if delete is not None:
        req["delete"] = delete
    if deleted is not None:
        req["deleted"] = deleted
    return card.Transaction(req)


@validate_card_object
def delete(card, file=None, note_id=None):
    """Delete a DB note in a Notefile by its ID.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The file name of the DB notefile.
        note_id (string): The id of the note to delete.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "note.delete"}
    if file:
        req["file"] = file
    if note_id:
        req["note"] = note_id
    return card.Transaction(req)


@validate_card_object
def update(card, file=None, note_id=None, body=None, payload=None):
    """Update a note in a DB Notefile by ID.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The file name of the DB notefile.
        note_id (string): The id of the note to update.
        body (JSON): The JSON object to add to the note.
        payload (string): The base64-encoded JSON payload to
            add to the note.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "note.get"}
    if file:
        req["file"] = file
    if note_id:
        req["note"] = note_id
    if body:
        req["body"] = body
    if payload:
        req["payload"] = payload
    return card.Transaction(req)
