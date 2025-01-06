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
def get(card, name=None):
    """Perform an env.get request against a Notecard.

    Args:
        card (Notecard): The current Notecard object.
        name (string): The name of an environment variable to get.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "env.get"}
    if name:
        req["name"] = name
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
