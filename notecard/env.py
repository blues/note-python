"""env Fluent API Helper.

This module contains helper methods for calling env.*
Notecard API commands.
"""
import notecard


def get(card, name=None):
    """Perform an env.get request against a Notecard.

    Args:
        name (string): The name of an environment variable to get.

    Returns:
        string: The result of the Notecard request.
    """
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "env.get"}
    if name:
        req["name"] = name
    return card.Transaction(req)
