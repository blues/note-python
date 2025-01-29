"""env Fluent API Helper."""

##
# @file env.py
#
# @brief env Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling env.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

import notecard
from notecard.validators import validate_card_object


@validate_card_object
def default(card, name=None, text=None):
    """Perform an env.default request against a Notecard.

    Args:
        card (Notecard): The current Notecard object.
        name (string): The name of an environment var to set a default for.
        text (optional): The default value. Omit to delete the default.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "env.default"}
    if name:
        req["name"] = name
    if text:
        req["text"] = text
    return card.Transaction(req)


@validate_card_object
def get(card, name=None, names=None, time=None):
    """Perform an env.get request against a Notecard.

    Args:
        card (Notecard): The current Notecard object.
        name (str, optional): The name of an environment variable to get.
        names (list, optional): List of environment variable names to retrieve.
        time (int, optional): UNIX epoch time to get variables modified after.

    Returns:
        dict: The result of the Notecard request containing either:
            - text: Value of the requested variable if name was specified
            - body: Object with name/value pairs if names was specified or
                   if neither name nor names was specified
            - time: UNIX epoch time of the last variable change
    """
    req = {"req": "env.get"}
    if name:
        req["name"] = name
    if names:
        req["names"] = names
    if time is not None:
        req["time"] = time
    return card.Transaction(req)


@validate_card_object
def modified(card):
    """Perform an env.modified request against a Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "env.modified"}
    return card.Transaction(req)


@validate_card_object
def set(card, name=None, text=None):
    """Perform an env.set request against a Notecard.

    Args:
        card (Notecard): The current Notecard object.
        name (string): The name of an environment variable to set.
        text (optional): The variable value. Omit to delete.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "env.set"}
    if name:
        req["name"] = name
    if text:
        req["text"] = text
    return card.Transaction(req)


@validate_card_object
def template(card, body=None):
    """Perform an env.template request against a Notecard.

    Args:
        card (Notecard): The current Notecard object.
        body (dict, optional): Schema with variable names and type hints.
            Supported type hints:
            - Boolean: true
            - String: numeric string for max length (pre v3.2.1)
            - Integer: 11-14, 18 (signed), 21-24 (unsigned)
            - Float: 12.1 (2-byte), 14.1 (4-byte), 18.1 (8-byte)

    Returns:
        dict: The result of the Notecard request, including 'bytes' field
            indicating storage size.

    Raises:
        ValueError: If type hints in body are invalid.
    """
    req = {"req": "env.template"}
    if body is not None:
        from .validators import validate_template_hints
        validate_template_hints(body)
        req["body"] = body
    return card.Transaction(req)
