"""hub Fluent API Helper."""

##
# @file hub.py
#
# @brief hub Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling hub.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def get(card):
    """Retrieve the current Notehub configuration for the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.get"}
    return card.Transaction(req)


@validate_card_object
def log(card, alert=None, sync=None, text=None):
    """Add a "device health" log message to send to Notehub on the next sync via the healthhost.qo Notefile.

    Args:
        card (Notecard): The current Notecard object.
        alert (bool): `true` if the message is urgent. This doesn't change any functionality, but rather `alert` is provided as a convenient flag to use in your program logic.
        sync (bool): `true` if a sync should be initiated immediately. Setting `true` will also remove the Notecard from certain types of penalty boxes.
        text (str): Text to log.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.log"}
    if alert is not None:
        req["alert"] = alert
    if sync is not None:
        req["sync"] = sync
    if text:
        req["text"] = text
    return card.Transaction(req)


@validate_card_object
def set(card, align=None, details=None, duration=None, host=None, inbound=None, mode=None, off=None, on=None, outbound=None, product=None, seconds=None, sn=None, sync=None, umin=None, uoff=None, uperiodic=None, version=None, vinbound=None, voutbound=None):
    r"""Use hub.set request is the primary method for controlling the Notecard's Notehub connection and sync behavior.

    Args:
        card (Notecard): The current Notecard object.
        align (bool): Use `true` to align syncs on a regular time-periodic cycle.
        details (str): When using Notecard LoRa you can use this argument to provide information about an alternative LoRaWAN server or service you would like the Notecard to use. The argument you provide must be a JSON object with three keys, "deveui", "appeui", and "appkey", all of which are hexadecimal strings with no leading 0x. For example: `{"deveui":"0080E11500088B37","appeui":"6E6F746563617264","appkey":"00088B37"}` The LoRaWAN details you send to a Notecard become part of its permanent configuration, and survive factory resets. You can reset a Notecard's LoRaWAN details to its default values by providing a `"-"` for the details argument.
        duration (int): When in `continuous` mode, the amount of time, in minutes, of each session (the minimum allowed value is `15`). When this time elapses, the Notecard gracefully ends the current session and starts a new one in order to sync session-specific data to Notehub.
        host (str): The URL of the Notehub service. Use `"-"` to reset to the default value.
        inbound (int): The max wait time, in minutes, to sync inbound data from Notehub. Explicit syncs (e.g. using `hub.sync`) do not affect this cadence. When in `periodic` or `continuous` mode this argument is required, otherwise the Notecard will function as if it is in `minimum` mode as it pertains to syncing behavior. Use `-1` to reset the value back to its default of `0`. A value of `0` means that the Notecard will never sync inbound data unless explicitly told to do so (e.g. using `hub.sync`).
        mode (str): The Notecard's synchronization mode. NOTE: The Notecard must be in `periodic` or `continuous` mode to use the onboard GPS module.
        off (bool): Set to `true` to manually instruct the Notecard to resume periodic mode after a web transaction has completed.
        on (bool): If in `periodic` mode, used to temporarily switch the Notecard to `continuous` mode to perform a web transaction.\n\nIgnored if the Notecard is already in `continuous` mode or if the Notecard is NOT performing a web transaction.
        outbound (int): The max wait time, in minutes, to sync outbound data from the Notecard. Explicit syncs (e.g. using `hub.sync`) do not affect this cadence. When in `periodic` or `continuous` mode this argument is required, otherwise the Notecard will function as if it is in `minimum` mode as it pertains to syncing behavior. Use `-1` to reset the value back to its default of `0`. A value of `0` means that the Notecard will never sync outbound data unless explicitly told to do so (e.g. using `hub.sync`).
        product (str): A Notehub-managed unique identifier that is used to match Devices with Projects. This string is used during a device's auto-provisioning to find the Notehub Project that, once provisioned, will securely manage the device and its data.
        seconds (int): If in `periodic` mode and using `on` above, the number of seconds to run in continuous mode before switching back to periodic mode. If not set, a default of 300 seconds is used. Ignored if the Notecard is already in continuous mode.
        sn (str): The end product's serial number.
        sync (bool): If in `continuous` mode, automatically and immediately sync each time an inbound Notefile change is detected on Notehub. NOTE: The `sync` argument is not supported when a Notecard is in NTN mode.
        umin (bool): Set to `true` to use USB/line power variable sync behavior, enabling the Notecard to stay in `continuous` mode when connected to USB/line power and fallback to `minimum` mode when disconnected.
        uoff (bool): Set to `true` to use USB/line power variable sync behavior, enabling the Notecard to stay in `continuous` mode when connected to USB/line power and fallback to `off` mode when disconnected.
        uperiodic (bool): Set to `true` to use USB/line power variable sync behavior, enabling the Notecard to stay in `continuous` mode when connected to USB/line power and fallback to `periodic` mode when disconnected.
        version (str): The version of your host firmware. The value provided will appear on your device in Notehub under the "Host Firmware" tab. You may pass a simple version number string (e.g. "1.0.0.0"), or an object with detailed information about the firmware image. If you provide an object it must take the following form. `{"org":"my-organization","product":"My Product","description":"A description of the image","version":"1.2.4","built":"Jan 01 2025 01:02:03","vermajor":1,"verminor":2,"verpatch":4,"verbuild": 5,"builder":"The Builder"}` If your project uses Notecard Outboard Firmware Update, you can alternatively use the `dfu.status` request to set your host firmware version.
        vinbound (str): Overrides `inbound` with a voltage-variable value. Use `"-"` to clear this value. NOTE: Setting voltage-variable values is not supported on Notecard XP.
        voutbound (str): Overrides `outbound` with a voltage-variable value. Use `"-"` to clear this value. NOTE: Setting voltage-variable values is not supported on Notecard XP.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.set"}
    if align is not None:
        req["align"] = align
    if details:
        req["details"] = details
    if duration is not None:
        req["duration"] = duration
    if host:
        req["host"] = host
    if inbound is not None:
        req["inbound"] = inbound
    if mode:
        req["mode"] = mode
    if off is not None:
        req["off"] = off
    if on is not None:
        req["on"] = on
    if outbound is not None:
        req["outbound"] = outbound
    if product:
        req["product"] = product
    if seconds is not None:
        req["seconds"] = seconds
    if sn:
        req["sn"] = sn
    if sync is not None:
        req["sync"] = sync
    if umin is not None:
        req["umin"] = umin
    if uoff is not None:
        req["uoff"] = uoff
    if uperiodic is not None:
        req["uperiodic"] = uperiodic
    if version:
        req["version"] = version
    if vinbound:
        req["vinbound"] = vinbound
    if voutbound:
        req["voutbound"] = voutbound
    return card.Transaction(req)


@validate_card_object
def signal(card, seconds=None):
    """Receive a Signal (a near-real-time Note) from Notehub. This request checks for an inbound signal from Notehub. If it finds a signal, this request returns the signal's body and deletes the signal. If there are multiple signals to receive, this request reads and deletes signals in FIFO (first in first out) order.

    Args:
        card (Notecard): The current Notecard object.
        seconds (int): The number of seconds to wait before timing out the request.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.signal"}
    if seconds is not None:
        req["seconds"] = seconds
    return card.Transaction(req)


@validate_card_object
def status(card):
    """Display the current status of the Notecard's connection to Notehub.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.status"}
    return card.Transaction(req)


@validate_card_object
def sync(card, allow=None, in_=None, out_=None):
    """Manually initiates a sync with Notehub.

    Args:
        card (Notecard): The current Notecard object.
        allow (bool): Set to `true` to remove the Notecard from certain types of penalty boxes (the default is `false`).
        in_ (bool): Set to `true` to only sync pending inbound Notefiles. Required when using NTN mode with Starnote to check for inbound Notefiles.
        out_ (bool): Set to `true` to only sync pending outbound Notefiles.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.sync"}
    if allow is not None:
        req["allow"] = allow
    if in_ is not None:
        req["in"] = in_
    if out_ is not None:
        req["out"] = out_
    return card.Transaction(req)


@validate_card_object
def syncStatus(card, sync=None):
    """Check on the status of a recently triggered or previous sync.

    Args:
        card (Notecard): The current Notecard object.
        sync (bool): `true` if this request should auto-initiate a sync pending outbound data.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "hub.sync.status"}
    if sync is not None:
        req["sync"] = sync
    return card.Transaction(req)
