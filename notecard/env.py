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
from .validators import validate_card_object


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
