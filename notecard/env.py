"""env Fluent API Helper.

This module contains helper methods for calling env.*
Notecard API commands.
"""
import notecard
from .validators import validate_card_object


@validate_card_object
def get(card, name=None):
    """Perform an env.get request against a Notecard.

    Args:
        name (string): The name of an environment variable to get.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "env.get"}
    if name:
        req["name"] = name
    return card.Transaction(req)
