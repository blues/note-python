"""env Fluent API Helper."""

##
# @file env.py
#
# @brief env Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling env.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def default(card, name=None, text=None):
    """Use by the Notecard host to specify a default value for an environment variable until that variable is overridden by a device, project or fleet-wide setting at Notehub.

    Args:
        card (Notecard): The current Notecard object.
        name (str): The name of the environment variable (case-insensitive).
        text (str): The value of the variable. Pass `""` or omit from the request to delete it.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "env.default"}
    if name:
        req["name"] = name
    if text:
        req["text"] = text
    return card.Transaction(req)


@validate_card_object
def get(card, name=None, names=None, time=None):
    """Return a single environment variable, or all variables according to precedence rules.

    Args:
        card (Notecard): The current Notecard object.
        name (str): The name of the environment variable (case-insensitive). Omit to return all environment variables known to the Notecard.
        names (list): A list of one or more variables to retrieve, by name (case-insensitive).
        time (int): Request a modified environment variable or variables from the Notecard, but only if modified after the time provided.

    Returns:
        dict: The result of the Notecard request.
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
def modified(card, time=None):
    """Get the time of the update to any environment variable managed by the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        time (int): Request whether the Notecard has detected an environment variable change since a known epoch time.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "env.modified"}
    if time is not None:
        req["time"] = time
    return card.Transaction(req)


@validate_card_object
def set(card, name=None, text=None):
    """Set a local environment variable on the Notecard. Local environment variables cannot be overridden by a Notehub variable of any scope.

    Args:
        card (Notecard): The current Notecard object.
        name (str): The name of the environment variable (case-insensitive).
        text (str): The value of the variable. Pass `""` or omit from the request to delete it.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "env.set"}
    if name:
        req["name"] = name
    if text:
        req["text"] = text
    return card.Transaction(req)


@validate_card_object
def template(card, body=None):
    """Use env.template request allows developers to provide a schema for the environment variables the Notecard uses. The provided template allows the Notecard to store environment variables as fixed-length binary records rather than as flexible JSON objects that require much more memory.

    Args:
        card (Notecard): The current Notecard object.
        body (dict): A sample JSON body that specifies environment variables names and values as "hints" for the data type. Possible data types are: boolean, integer, float, and string. See Understanding Template Data Types for a full explanation of type hints.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "env.template"}
    if body:
        req["body"] = body
    return card.Transaction(req)
