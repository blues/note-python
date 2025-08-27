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
def add(card, binary=None, body=None, file=None, full=None, key=None, limit=None, live=None, max=None, note=None, payload=None, sync=None, verify=None):
    """Add a Note to a Notefile, creating the Notefile if it doesn't yet exist.

    Args:
        card (Notecard): The current Notecard object.
        binary (bool): If `true`, the Notecard will send all the data in the binary buffer to Notehub. Learn more in this guide on Sending and Receiving Large Binary Objects.
        body (dict): A JSON object to be enqueued. A Note must have either a `body` or a `payload`, and can have both.
        file (str): The name of the Notefile. On Notecard LoRa this argument is required. On all other Notecards this field is optional and defaults to `data.qo` if not provided. When using this request on the Notecard the Notefile name must end in one of: `.qo` for a queue outgoing (Notecard to Notehub) with plaintext transport `.qos` for a queue outgoing with encrypted transport `.db` for a bidirectionally synchronized database with plaintext transport `.dbs` for a bidirectionally synchronized database with encrypted transport `.dbx` for a local-only database
        full (bool): If set to `true`, and the Note is using a Notefile Template, the Note will bypass usage of omitempty and retain `null`, `0`, `false`, and empty string `""` values.
        key (str): The name of an environment variable in your Notehub.io project that contains the contents of a public key. Used when encrypting the Note body for transport.
        limit (bool): If set to `true`, the Note will not be created if Notecard is in a penalty box.
        live (bool): If `true`, bypasses saving the Note to flash on the Notecard. Required to be set to `true` if also using `"binary":true`.
        max (int): Defines the maximum number of queued Notes permitted in the specified Notefile (`"file"`). Any Notes added after this value will be rejected. When used with `"sync":true`, a sync will be triggered when the number of pending Notes matches the `max` value.
        note (str): If the Notefile has a `.db/.dbs/.dbx` extension, specifies a unique Note ID. If `note` string is `"?"`, then a random unique Note ID is generated and returned as `{"note":"xxx"}`. If this argument is provided for a `.qo` Notefile, an error is returned.
        payload (str): A base64-encoded binary payload. A Note must have either a `body` or a `payload`, and can have both. If a Note template is not in use, payloads are limited to 250 bytes.
        sync (bool): Set to `true` to sync immediately. Only applies to outgoing Notecard requests, and only guarantees syncing the specified Notefile. Auto-syncing incoming Notes from Notehub is set on the Notecard with `{"req": "hub.set", "mode":"continuous", "sync": true}`.
        verify (bool): If set to `true` and using a templated Notefile, the Notefile will be written to flash immediately, rather than being cached in RAM and written to flash later.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "note.add"}
    if binary is not None:
        req["binary"] = binary
    if body:
        req["body"] = body
    if file:
        req["file"] = file
    if full is not None:
        req["full"] = full
    if key:
        req["key"] = key
    if limit is not None:
        req["limit"] = limit
    if live is not None:
        req["live"] = live
    if max is not None:
        req["max"] = max
    if note:
        req["note"] = note
    if payload:
        req["payload"] = payload
    if sync is not None:
        req["sync"] = sync
    if verify is not None:
        req["verify"] = verify
    return card.Transaction(req)


@validate_card_object
def changes(card, delete=None, deleted=None, file, max=None, reset=None, start=None, stop=None, tracker=None):
    """Use to incrementally retrieve changes within a specific Notefile.

    Args:
        card (Notecard): The current Notecard object.
        delete (bool): `true` to delete the Notes returned by the request.
        deleted (bool): `true` to return deleted Notes with this request. Deleted Notes are only persisted in a database notefile (`.db/.dbs`) between the time of Note deletion on the Notecard and the time that a sync with Notehub takes place. As such, this boolean will have no effect after a sync or on queue notefiles (`.q*`).
        file (str): The Notefile ID.
        max (int): The maximum number of Notes to return in the request.
        reset (bool): `true` to reset a change tracker.
        start (bool): `true` to reset the tracker to the beginning.
        stop (bool): `true` to delete the tracker.
        tracker (str): The change tracker ID. This value is developer-defined and can be used across both the `note.changes` and `file.changes` requests.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "note.changes"}
    if delete is not None:
        req["delete"] = delete
    if deleted is not None:
        req["deleted"] = deleted
    if file:
        req["file"] = file
    if max is not None:
        req["max"] = max
    if reset is not None:
        req["reset"] = reset
    if start is not None:
        req["start"] = start
    if stop is not None:
        req["stop"] = stop
    if tracker:
        req["tracker"] = tracker
    return card.Transaction(req)


@validate_card_object
def delete(card, file, note, verify=None):
    """Delete a Note from a DB Notefile by its Note ID. To delete Notes from a `.qi` Notefile, use `note.get` or `note.changes` with `delete:true`.

    Args:
        card (Notecard): The current Notecard object.
        file (str): The Notefile from which to delete a Note. Must be a Notefile with a `.db` or `.dbx` extension.
        note (str): The Note ID of the Note to delete.
        verify (bool): If set to `true` and using a templated Notefile, the Notefile will be written to flash immediately, rather than being cached in RAM and written to flash later.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "note.delete"}
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    if verify is not None:
        req["verify"] = verify
    return card.Transaction(req)


@validate_card_object
def get(card, decrypt=None, delete=None, deleted=None, file=None, note=None):
    """Retrieve a Note from a Notefile. The file must either be a DB Notefile or inbound queue file (see `file` argument below). `.qo`/`.qos` Notes must be read from the Notehub event table using the Notehub Event API.

    Args:
        card (Notecard): The current Notecard object.
        decrypt (bool): `true` to decrypt encrypted inbound Notefiles.
        delete (bool): `true` to delete the Note after retrieving it.
        deleted (bool): `true` to allow retrieval of a deleted Note.
        file (str): The Notefile name must end in `.qi` (for plaintext transport), `.qis` (for encrypted transport), `.db` or `.dbx` (for local-only DB Notefiles).
        note (str): If the Notefile has a `.db` or `.dbx` extension, specifies a unique Note ID. Not applicable to `.qi` Notefiles.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "note.get"}
    if decrypt is not None:
        req["decrypt"] = decrypt
    if delete is not None:
        req["delete"] = delete
    if deleted is not None:
        req["deleted"] = deleted
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    return card.Transaction(req)


@validate_card_object
def template(card, body=None, delete=None, file, format=None, length=None, port=None, verify=None):
    """By using the `note.template` request with any `.qo`/`.qos` Notefile, developers can provide the Notecard with a schema of sorts to apply to future Notes added to the Notefile. This template acts as a hint to the Notecard that allows it to internally store data as fixed-length binary records rather than as flexible JSON objects which require much more memory. Using templated Notes in place of regular Notes increases the storage and sync capability of the Notecard by an order of magnitude. Read about Working with Note Templates for additional information.

    Args:
        card (Notecard): The current Notecard object.
        body (dict): A sample JSON body that specifies field names and values as "hints" for the data type. Possible data types are: boolean, integer, float, and string. See Understanding Template Data Types for an explanation of type hints and explanations.
        delete (bool): Set to `true` to delete all pending Notes using the template if one of the following scenarios is also true: Connecting via non-NTN (e.g. cellular or Wi-Fi) communications, but attempting to sync NTN-compatible Notefiles. or Connecting via NTN (e.g. satellite) communications, but attempting to sync non-NTN-compatible Notefiles. Read more about this feature in Starnote Best Practices.
        file (str): The name of the Notefile to which the template will be applied.
        format (str): By default all Note templates automatically include metadata, including a timestamp for when the Note was created, various fields about a device's location, as well as a timestamp for when the device's location was determined. By providing a `format` of `"compact"` you tell the Notecard to omit this additional metadata to save on storage and bandwidth. The use of `format: "compact"` is required for Notecard LoRa and a Notecard paired with Starnote. When using `"compact"` templates, you may include the following keywords in your template to add in fields that would otherwise be omitted: `lat`, `lon`, `ltime`, `time`. See Creating Compact Templates to learn more.
        length (int): The maximum length of a `payload` (in bytes) that can be sent in Notes for the template Notefile. As of v3.2.1 `length` is not required, and payloads can be added to any template-based Note without specifying the payload length.
        port (int): This argument is required on Notecard LoRa and a Notecard paired with Starnote, but ignored on all other Notecards. A port is a unique integer in the range 1–100, where each unique number represents one Notefile. This argument allows the Notecard to send a numerical reference to the Notefile over the air, rather than the full Notefile name. The port you provide is also used in the "frame port" field on LoRaWAN gateways.
        verify (bool): If `true`, returns the current template set on a given Notefile.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "note.template"}
    if body:
        req["body"] = body
    if delete is not None:
        req["delete"] = delete
    if file:
        req["file"] = file
    if format:
        req["format"] = format
    if length is not None:
        req["length"] = length
    if port is not None:
        req["port"] = port
    if verify is not None:
        req["verify"] = verify
    return card.Transaction(req)


@validate_card_object
def update(card, body=None, file, note, payload=None, verify=None):
    """Update a Note in a DB Notefile by its ID, replacing the existing `body` and/or `payload`.

    Args:
        card (Notecard): The current Notecard object.
        body (dict): A JSON object to add to the Note. A Note must have either a `body` or `payload`, and can have both.
        file (str): The name of the DB Notefile that contains the Note to update.
        note (str): The unique Note ID.
        payload (str): A base64-encoded binary payload. A Note must have either a `body` or `payload`, and can have both.
        verify (bool): If set to `true` and using a templated Notefile, the Notefile will be written to flash immediately, rather than being cached in RAM and written to flash later.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "note.update"}
    if body:
        req["body"] = body
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    if payload:
        req["payload"] = payload
    if verify is not None:
        req["verify"] = verify
    return card.Transaction(req)
