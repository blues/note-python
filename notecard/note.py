"""note Fluent API Helper."""

##
# @file note.py
#
# @brief note Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling note.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def add(card, file=None, body=None, payload=None, binary=None,
        sync=None, port=None):
    """Add a Note to a Notefile.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The name of the file.
        body (dict): A JSON object containing the note data.
        payload (string): An optional base64-encoded string.
        binary (bool): When True, indicates that the note's payload field
            contains binary data that should be base64-encoded.
        sync (bool): Perform an immediate sync after adding.
        port (int): If provided, a unique number to represent a notefile.
            Required for Notecard LoRa.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "note.add"}
    if file:
        req["file"] = file
    if body:
        req["body"] = body
    if payload:
        req["payload"] = payload
    if port:
        if not isinstance(port, int):
            return {"err": "port parameter must be an integer"}
        req["port"] = port
    if sync is not None:
        if not isinstance(sync, bool):
            return {"err": "sync parameter must be a boolean"}
        req["sync"] = sync
    if binary is not None:
        if not isinstance(binary, bool):
            return {"err": "binary parameter must be a boolean"}
        req["binary"] = binary

    return card.Transaction(req)


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
        if not isinstance(maximum, int):
            return {"err": "maximum parameter must be an integer"}
        req["max"] = maximum
    if start is not None:
        if not isinstance(start, bool):
            return {"err": "start parameter must be a boolean"}
        req["start"] = start
    if stop is not None:
        if not isinstance(stop, bool):
            return {"err": "stop parameter must be a boolean"}
        req["stop"] = stop
    if deleted is not None:
        if not isinstance(deleted, bool):
            return {"err": "deleted parameter must be a boolean"}
        req["deleted"] = deleted
    if delete is not None:
        if not isinstance(delete, bool):
            return {"err": "delete parameter must be a boolean"}
        req["delete"] = delete
    return card.Transaction(req)


@validate_card_object
def get(card, file="data.qi", note_id=None, delete=None, deleted=None):
    """Retrieve a note from an inbound or DB Notefile.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The inbound or DB notefile to retrieve a
            Notefile from.
        note_id (string): (DB files only) The ID of the note to retrieve.
        delete (bool): Whether to delete the note after retrieval.
        deleted (bool): Whether to allow retrieval of a deleted note.

    Returns:
        dict: The result of the Notecard request. If binary data is present,
        the 'binary' field contains the decoded data.
    """
    req = {"req": "note.get"}
    req["file"] = file
    if note_id:
        req["note"] = note_id
    if delete is not None:
        if not isinstance(delete, bool):
            return {"err": "delete parameter must be a boolean"}
        req["delete"] = delete
    if deleted is not None:
        if not isinstance(deleted, bool):
            return {"err": "deleted parameter must be a boolean"}
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
    req = {"req": "note.update"}
    if file:
        req["file"] = file
    if note_id:
        req["note"] = note_id
    if body:
        req["body"] = body
    if payload:
        req["payload"] = payload
    return card.Transaction(req)


@validate_card_object
def template(
        card,
        *,  # Force keyword arguments for clarity
        file=None,
        body=None,
        length=None,
        port=None,
        format=None,
        compact=None,
        verify=None,
        delete=None):
    """Create a template for new Notes in a Notefile.

    Args:
        card (Notecard): The current Notecard object.
        file (string): The file name of the notefile.
        body (dict): A sample JSON body that specifies field names and
            values as type hints. Supported: bool, int, float, str.
        length (int): If provided, the maximum length of a payload that
            can be sent in Notes for the template Notefile.
        port (int): If provided, a unique number to represent a notefile.
            Required for Notecard LoRa.
        format (string): If "compact", omits additional metadata to save
            storage and bandwidth.
        compact (bool): Legacy parameter. If True, equivalent to setting
            format="compact". Retained for backward compatibility.
        verify (bool): When True, verifies the template against existing
            notes in the Notefile.
        delete (bool): When True, deletes the template from the Notefile.

    Returns:
        dict: The result of the Notecard request. Returns error object if
        validation fails.
    """
    req = {"req": "note.template"}
    if file:
        req["file"] = file

    if body:
        # Validate that all values in body are of supported types
        def validate_value(val):
            if isinstance(val, (bool, int, float, str)):
                return True
            if isinstance(val, (list, tuple)):
                return all(isinstance(x, (bool, int, float, str)) for x in val)
            return False

        for key, value in body.items():
            if not validate_value(value):
                return {
                    "err": "Body values must be boolean, integer, float, "
                           "or string"
                }
        req["body"] = body

    if length is not None:
        if not isinstance(length, int):
            return {"err": "length parameter must be an integer"}
        req["length"] = length

    if port is not None:
        if not isinstance(port, int):
            return {"err": "port parameter must be an integer"}
        req["port"] = port

    if compact is True:
        format = "compact"

    if format == "compact":
        req["format"] = "compact"

    if verify is not None:
        if not isinstance(verify, bool):
            return {"err": "verify parameter must be a boolean"}
        req["verify"] = verify
    if delete is not None:
        if not isinstance(delete, bool):
            return {"err": "delete parameter must be a boolean"}
        req["delete"] = delete

    return card.Transaction(req)
