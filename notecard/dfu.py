"""dfu Fluent API Helper."""

##
# @file dfu.py
#
# @brief dfu Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling dfu.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def get(card, length=None, offset=None):
    """Retrieve downloaded firmware data from the Notecard for use with IAP host MCU firmware updates.

    Args:
        card (Notecard): The current Notecard object.
        length (int): The number of bytes of firmware data to read and return to the host. Set to `0` to verify that the Notecard is in DFU mode without attempting to retrieve data.
        offset (int): The offset to use before performing a read of firmware data.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "dfu.get"}
    if length is not None:
        req["length"] = length
    if offset is not None:
        req["offset"] = offset
    return card.Transaction(req)


@validate_card_object
def status(card, name=None, stop=None, status=None, version=None, vvalue=None, on=None, off=None, err=None):
    """Get and sets the background download status of MCU host or Notecard firmware updates.

    Args:
        card (Notecard): The current Notecard object.
        name (str): Determines which type of firmware update status to view. The value can be `"user"` (default), which gets the status of MCU host firmware updates, or `"card"`, which gets the status of Notecard firmware updates.
        stop (bool): `true` to clear DFU state and delete the local firmware image from the Notecard.
        status (str): When setting `stop` to `true`, an optional string synchronized to Notehub, which can be used for informational or diagnostic purposes.
        version (str): Version information on the host firmware to pass to Notehub. You may pass a simple version number string (e.g. `"1.0.0.0"`), or an object with detailed information about the firmware image (recommended).
        vvalue (str): A voltage-variable string that controls, by Notecard voltage, whether or not DFU is enabled. Use a boolean `1` (on) or `0` (off) for each source/voltage level: `usb:<1/0>;high:<1/0>;normal:<1/0>;low:<1/0>;dead:0`.
        on (bool): `true` to allow firmware downloads from Notehub.
        off (bool): `true` to disable firmware downloads from Notehub.
        err (str): If `err` text is provided along with `"stop":true`, this sets the host DFU to an error state with the specified string.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "dfu.status"}
    if name:
        req["name"] = name
    if stop is not None:
        req["stop"] = stop
    if status:
        req["status"] = status
    if version:
        req["version"] = version
    if vvalue:
        req["vvalue"] = vvalue
    if on is not None:
        req["on"] = on
    if off is not None:
        req["off"] = off
    if err:
        req["err"] = err
    return card.Transaction(req)
