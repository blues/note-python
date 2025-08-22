"""card Fluent API Helper."""

##
# @file card.py
#
# @brief card Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling card.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def attn(card, files=None, mode=None, off=None, on=None, payload=None, seconds=None, start=None, verify=None):
    """Configure hardware notification from the Notecard to MCU host. NOTE: Requires a connection between the Notecard ATTN pin and a GPIO pin on the host MCU.

    Args:
        card (Notecard): The current Notecard object.
        files (list): A list of Notefiles to watch for file-based interrupts.
        mode (str): A comma-separated list of one or more of the following keywords. Some keywords are only supported on certain types of Notecards.
        off (bool): When `true`, completely disables ATTN processing and sets the pin OFF. This setting is retained across device restarts.
        on (bool): When `true`, enables ATTN processing. This setting is retained across device restarts.
        payload (str): When using `sleep` mode, a payload of data from the host that the Notecard should hold in memory until retrieved by the host.
        seconds (int): To set an ATTN timeout when arming, or when using `sleep`. NOTE: When the Notecard is in `continuous` mode, the `seconds` timeout is serviced by a routine that wakes every 15 seconds. You can predict when the device will wake, by rounding up to the nearest 15 second interval.
        start (bool): When using `sleep` mode and the host has reawakened, request the Notecard to return the stored `payload`.
        verify (bool): When `true`, returns the current attention mode configuration, if any.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.attn"}
    if files:
        req["files"] = files
    if mode:
        req["mode"] = mode
    if off is not None:
        req["off"] = off
    if on is not None:
        req["on"] = on
    if payload:
        req["payload"] = payload
    if seconds is not None:
        req["seconds"] = seconds
    if start is not None:
        req["start"] = start
    if verify is not None:
        req["verify"] = verify
    return card.Transaction(req)


@validate_card_object
def aux(card, mode=None, usage=None, seconds=None, max=None, start=None, gps=None, rate=None, sync=None, file=None, connected=None, limit=None, sensitivity=None, ms=None, count=None, offset=None):
    """Configure various uses of the general-purpose I/O (GPIO) pins `AUX1`-`AUX4` on the Notecard edge connector for tracking applications and simple GPIO sensing and counting tasks.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): The AUX mode. Must be one of the following keywords. Some keywords are only supported on certain types of Notecards.
        usage (list): An ordered list of pin modes for each AUX pin when in GPIO mode.
        seconds (int): When in `gpio` mode, if an `AUX` pin is configured as a `count` type, the count of rising edges can be broken into samples of this duration. Passing `0` or omitting this field will total into a single sample.
        max (int): When in `gpio` mode, if an `AUX` pin is configured as a `count` type, the maximum number of samples of duration `seconds`, after which all subsequent counts are added to the final sample. Passing `0` or omitting this value will provide a single incrementing count of rising edges on the pin.
        start (bool): When in `gpio` mode, if an `AUX` pin is configured as a `count` type, set to `true` to reset counters and start incrementing.
        gps (bool): If `true`, along with `"mode":"track"` the Notecard supports the use of an external GPS module. This argument is deprecated. Use the `card.aux.serial` request with a `mode` of `"gps"` instead.
        rate (int): The AUX UART baud rate for debug communication over the AUXRX and AUXTX pins.
        sync (bool): If `true`, for pins set as `input` by `usage`, the Notecard will autonomously report any state changes as new notes in `file`. For pins used as `counter`, the Notecard will use an interrupt to count pulses and will report the total in a new note in `file` unless it has been noted in the previous second.
        file (str): The name of the Notefile used to report state changes when used in conjunction with `"sync": true`. Default Notefile name is `_button.qo`.
        connected (bool): If `true`, defers the sync of the state change Notefile to the next sync as configured by the `hub.set` request.
        limit (bool): If `true`, along with `"mode":"track"` and `gps:true` the Notecard will disable concurrent modem use during GPS tracking.
        sensitivity (int): When used with `"mode":"neo-monitor"` or `"mode":"track-neo-monitor"`, this controls the brightness of NeoPixel lights, where `100` is the maximum brightness and `1` is the minimum.
        ms (int): When in `gpio` mode, this argument configures a debouncing interval. With a debouncing interval in place, the Notecard excludes all transitions with a shorter duration than the provided debounce time, in milliseconds. This interval only applies to GPIOs configured with a `usage` of `count`, `count-pulldown`, or `count-pullup`.
        count (int): When used with `"mode":"neo-monitor"` or `"mode":"track-neo-monitor"`, this controls the number of NeoPixels to use in a strip. Possible values are `1`, `2`, or `5`.
        offset (int): When used with `"mode":"neo-monitor"` or `"mode":"track-neo-monitor"`, this is the 1-based index in a strip of NeoPixels that determines which single NeoPixel the host can command.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.aux"}
    if mode:
        req["mode"] = mode
    if usage:
        req["usage"] = usage
    if seconds is not None:
        req["seconds"] = seconds
    if max is not None:
        req["max"] = max
    if start is not None:
        req["start"] = start
    if gps is not None:
        req["gps"] = gps
    if rate is not None:
        req["rate"] = rate
    if sync is not None:
        req["sync"] = sync
    if file:
        req["file"] = file
    if connected is not None:
        req["connected"] = connected
    if limit is not None:
        req["limit"] = limit
    if sensitivity is not None:
        req["sensitivity"] = sensitivity
    if ms is not None:
        req["ms"] = ms
    if count is not None:
        req["count"] = count
    if offset is not None:
        req["offset"] = offset
    return card.Transaction(req)


@validate_card_object
def auxSerial(card, mode=None, duration=None, rate=None, limit=None, max=None, ms=None, minutes=None):
    """Configure various uses of the AUXTX and AUXRX pins on the Notecard's edge connector.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): The AUX mode. Must be one of the following:
        duration (int): If using `"mode": "accel"`, specify a sampling duration for the Notecard accelerometer.
        rate (int): The baud rate or speed at which information is transmitted over AUX serial. The default is `115200` unless using GPS, in which case the default is `9600`.
        limit (bool): If `true`, along with `"mode":"gps"` the Notecard will disable concurrent modem use during GPS tracking.
        max (int): The maximum amount of data to send per session, in bytes. This is typically set to the size of the receive buffer on the host minus `1`. For example, `note-arduino` uses a buffer size of `(SERIALRXBUFFER_SIZE - 1)`.
        ms (int): The delay in milliseconds before sending a buffer of `max` size.
        minutes (int): When using `"mode": "notify,dfu"`, specify an interval for notifying the host.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.aux.serial"}
    if mode:
        req["mode"] = mode
    if duration is not None:
        req["duration"] = duration
    if rate is not None:
        req["rate"] = rate
    if limit is not None:
        req["limit"] = limit
    if max is not None:
        req["max"] = max
    if ms is not None:
        req["ms"] = ms
    if minutes is not None:
        req["minutes"] = minutes
    return card.Transaction(req)


@validate_card_object
def binaryGet(card, cobs=None, offset=None, length=None):
    """Return binary data stored in the binary storage area of the Notecard. The response to this API command first returns the JSON-formatted response object, then the binary data. See the guide on Sending and Receiving Large Binary Objects for best practices when using `card.binary`.

    Args:
        card (Notecard): The current Notecard object.
        cobs (int): The size of the COBS-encoded data you are expecting to be returned (in bytes).
        offset (int): Used along with `length`, the number of bytes to offset the binary payload from 0 when retrieving binary data from the binary storage area of the Notecard. Primarily used when retrieving multiple fragments of a binary payload from the Notecard.
        length (int): Used along with `offset`, the number of bytes to retrieve from the binary storage area of the Notecard.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.binary.get"}
    if cobs is not None:
        req["cobs"] = cobs
    if offset is not None:
        req["offset"] = offset
    if length is not None:
        req["length"] = length
    return card.Transaction(req)


@validate_card_object
def binaryPut(card, offset=None, cobs=None, status=None):
    """Add binary data to the binary storage area of the Notecard. The Notecard expects to receive binary data immediately following the usage of this API command. See the guide on Sending and Receiving Large Binary Objects for best practices when using `card.binary`.

    Args:
        card (Notecard): The current Notecard object.
        offset (int): The number of bytes to offset the binary payload from 0 when appending the binary data to the binary storage area of the Notecard. Primarily used when sending multiple fragments of one binary payload to the Notecard.
        cobs (int): The size of the COBS-encoded data (in bytes).
        status (str): The MD5 checksum of the data, before it has been encoded.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.binary.put"}
    if offset is not None:
        req["offset"] = offset
    if cobs is not None:
        req["cobs"] = cobs
    if status:
        req["status"] = status
    return card.Transaction(req)


@validate_card_object
def binary(card, delete=None):
    """View the status of the binary storage area of the Notecard and optionally clear any data and related `card.binary` variables. See the guide on Sending and Receiving Large Binary Objects for best practices when using `card.binary`.

    Args:
        card (Notecard): The current Notecard object.
        delete (bool): Clear the COBS area on the Notecard and reset all related arguments previously set by a card.binary request.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.binary"}
    if delete is not None:
        req["delete"] = delete
    return card.Transaction(req)


@validate_card_object
def carrier(card, mode=None):
    """Use the `AUX_CHARGING` pin on the Notecard edge connector to notify the Notecard that the pin is connected to a Notecarrier that supports charging, using open-drain. Once set, `{"charging":true}` will appear in a response if the Notecarrier is currently indicating that charging is in progress.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): The `AUXCHARGING` mode. Set to `"charging"` to tell the Notecard that `AUXCHARGING` is connected to a Notecarrier that supports charging on `AUXCHARGING`. Set to `"-"` or `"off"` to turn off the `AUXCHARGING` detection.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.carrier"}
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def contact(card, name=None, org=None, role=None, email=None):
    """Use to set or retrieve information about the Notecard maintainer. Once set, this information is synced to Notehub.

    Args:
        card (Notecard): The current Notecard object.
        name (str): Set the name of the Notecard maintainer.
        org (str): Set the organization name of the Notecard maintainer.
        role (str): Set the role of the Notecard maintainer.
        email (str): Set the email address of the Notecard maintainer.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.contact"}
    if name:
        req["name"] = name
    if org:
        req["org"] = org
    if role:
        req["role"] = role
    if email:
        req["email"] = email
    return card.Transaction(req)


@validate_card_object
def dfu(card, name=None, on=None, off=None, seconds=None, stop=None, start=None, mode=None):
    """Use to configure a Notecard for Notecard Outboard Firmware Update.

    Args:
        card (Notecard): The current Notecard object.
        name (str): One of the supported classes of host MCU. Supported MCU classes are `"esp32"`, `"stm32"`, `"stm32-bi"`, `"mcuboot"` (added in v5.3.1), and `"-"`, which resets the configuration. The "bi" in `"stm32-bi"` stands for "boot inverted", and the `"stm32-bi"` option should be used on STM32 family boards where the hardware boot pin is assumed to be active low, instead of active high. Supported MCUs can be found on the Notecarrier F datasheet.
        on (bool): Set to `true` to enable Notecard Outboard Firmware Update.
        off (bool): Set to `true` to disable Notecard Outboard Firmware Update from occurring.
        seconds (int): When used with `"off":true`, disable Notecard Outboard Firmware Update operations for the specified number of `seconds`.
        stop (bool): Set to `true` to disable the host RESET that is normally performed on the host MCU when the Notecard starts up (in order to ensure a clean startup), and also when the Notecard wakes up the host MCU after the expiration of a `card.attn` "sleep" operation. If `true`, the host MCU will not be reset in these two conditions.
        start (bool): Set to `true` to enable the host RESET if previously disabled with `"stop":true`.
        mode (str): The `mode` argument allows you to control whether a Notecard's `AUX` pins (default) or `ALTDFU` pins are used for Notecard Outboard Firmware Update. This argument is only supported on Notecards that have `ALTDFU` pins, which includes all versions of Notecard Cell+WiFi, non-legacy versions of Notecard Cellular, and Notecard WiFi v2.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.dfu"}
    if name:
        req["name"] = name
    if on is not None:
        req["on"] = on
    if off is not None:
        req["off"] = off
    if seconds is not None:
        req["seconds"] = seconds
    if stop is not None:
        req["stop"] = stop
    if start is not None:
        req["start"] = start
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def illumination(card):
    """Use request returns an illumination reading (in lux) from an OPT3001 ambient light sensor connected to Notecard's I2C bus. If no OPT3001 sensor is detected, this request returns an “illumination sensor is not available” error.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.illumination"}
    return card.Transaction(req)


@validate_card_object
def io(card, i2c=None, mode=None):
    """Can be used to override the Notecard's I2C address from its default of `0x17` and change behaviors of the onboard LED and USB port.

    Args:
        card (Notecard): The current Notecard object.
        i2c (int): The alternate address to use for I2C communication. Pass `-1` to reset to the default address
        mode (str): The mode parameter.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.io"}
    if i2c is not None:
        req["i2c"] = i2c
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def led(card, mode=None, on=None, off=None):
    """Use along with the card.aux API to turn connected LEDs on/off or to manage a single connected NeoPixel. If using monochromatic LEDs, they must be wired according to the instructions provided in the guide on Using Monitor Mode. Please note that the use of monochromatic LEDs is not supported by Notecard for LoRa. If using NeoPixels, the NeoPixel (or strip of NeoPixels) must be wired according to the instructions provided in the guide on Using Neo-Monitor Mode.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): Used to specify the color of the LED to turn on or off. For LEDs, possible values are `"red"`, `"green"`, and `"yellow"`. For NeoPixels, possible values are `"red"`, `"green"`, `"blue"`, `"yellow"`, `"cyan"`, `"magenta"`, `"orange"`, `"white"`, and `"gray"`.
        on (bool): Set to `true` to turn the specified LED or NeoPixel on.
        off (bool): Set to `true` to turn the specified LED or NeoPixel off.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.led"}
    if mode:
        req["mode"] = mode
    if on is not None:
        req["on"] = on
    if off is not None:
        req["off"] = off
    return card.Transaction(req)


@validate_card_object
def locationMode(card, mode=None, seconds=None, vseconds=None, lat=None, lon=None, max=None, delete=None, minutes=None, threshold=None):
    """Set location-related configuration settings. Retrieves the current location mode when passed with no argument.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): Must be one of: `""` to retrieve the current mode. `"off"` to turn location mode off. Approximate location may still be ascertained from Notehub. `"periodic"` to sample location at a specified interval, if the device has moved. `"continuous"` to enable the Notecard's GPS/GNSS module for continuous sampling. When in continuous mode the Notecard samples a new GPS/GNSS reading for every new Note. `"fixed"` to report the location as a fixed location using the specified `lat` and `lon` coordinates. This is the only supported mode on Notecard LoRa.
        seconds (int): When in `periodic` mode, location will be sampled at this interval, if the Notecard detects motion. If seconds is < 300, during periods of sustained movement the Notecard will leave its onboard GPS/GNSS on continuously to avoid powering the module on and off repeatedly.
        vseconds (str): In `periodic` mode, overrides `seconds` with a voltage-variable value.
        lat (float): When in periodic or continuous mode, providing this value enables geofencing. The value you provide for this argument should be the latitude of the center of the geofence, in degrees. When in fixed mode, the value you provide for this argument should be the latitude location of the device itself, in degrees.
        lon (float): When in periodic or continuous mode, providing this value enables geofencing. The value you provide for this argument should be the longitude of the center of the geofence, in degrees. When in fixed mode, the value you provide for this argument should be the longitude location of the device itself, in degrees.
        max (int): Meters from a geofence center. Used to enable geofence location tracking.
        delete (bool): Set to `true` to delete the last known location stored in the Notecard.
        minutes (int): When geofence is enabled, the number of minutes the device should be outside the geofence before the Notecard location is tracked.
        threshold (int): When in `periodic` mode, the number of motion events (registered by the built-in accelerometer) required to trigger GPS to turn on.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.location.mode"}
    if mode:
        req["mode"] = mode
    if seconds is not None:
        req["seconds"] = seconds
    if vseconds:
        req["vseconds"] = vseconds
    if lat is not None:
        req["lat"] = lat
    if lon is not None:
        req["lon"] = lon
    if max is not None:
        req["max"] = max
    if delete is not None:
        req["delete"] = delete
    if minutes is not None:
        req["minutes"] = minutes
    if threshold is not None:
        req["threshold"] = threshold
    return card.Transaction(req)


@validate_card_object
def location(card):
    """Retrieve the last known location of the Notecard and the time at which it was acquired. Use card.location.mode to configure location settings. This request will return the cell tower location or triangulated location of the most recent session if a GPS/GNSS location is not available. On Notecard LoRa this request can only return a location set through the card.location.mode request's `"fixed"` mode.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.location"}
    return card.Transaction(req)


@validate_card_object
def locationTrack(card, start=None, heartbeat=None, hours=None, sync=None, stop=None, file=None, payload=None):
    """Store location data in a Notefile at the `periodic` interval, or using a specified `heartbeat`. This request is only available when the `card.location.mode` request has been set to `periodic`—e.g. `{"req":"card.location.mode","mode":"periodic","seconds":300}`. If you want to track and transmit data simultaneously consider using an external GPS/GNSS module with the Notecard. If you connect a BME280 sensor on the I2C bus, Notecard will include a temperature, humidity, and pressure reading with each captured Note. If you connect an ENS210 sensor on the I2C bus, Notecard will include a temperature and pressure reading with each captured Note. Learn more in _track.qo.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): Set to `true` to start Notefile tracking.
        heartbeat (bool): When `start` is `true`, set to `true` to enable tracking even when motion is not detected. If using `heartbeat`, also set the `hours` below.
        hours (int): If `heartbeat` is true, add a heartbeat entry at this hourly interval. Use a negative integer to specify a heartbeat in minutes instead of hours.
        sync (bool): Set to `true` to perform an immediate sync to the Notehub each time a new Note is added.
        stop (bool): Set to `true` to stop Notefile tracking.
        file (str): The Notefile in which to store tracked location data. See the `_track.qo` Notefile's documentation for details on the format of the data captured.
        payload (str): A base64-encoded binary payload to be included in the next `_track.qo` Note. See the guide on Sampling at Predefined Intervals for more details.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.location.track"}
    if start is not None:
        req["start"] = start
    if heartbeat is not None:
        req["heartbeat"] = heartbeat
    if hours is not None:
        req["hours"] = hours
    if sync is not None:
        req["sync"] = sync
    if stop is not None:
        req["stop"] = stop
    if file:
        req["file"] = file
    if payload:
        req["payload"] = payload
    return card.Transaction(req)


@validate_card_object
def monitor(card, mode=None, count=None, usb=None):
    """When a Notecard is in monitor mode, this API is used to configure the general-purpose `AUX1`-`AUX4` pins to test and monitor Notecard activity.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): Can be set to one of `green`, `red` or `yellow` to temporarily override the behavior of an AUX pin LED. See Using Monitor Mode for additional details.
        count (int): The number of pulses to send to the overridden AUX pin LED. Set this value to `0` to return the LED to its default behavior.
        usb (bool): Set to `true` to configure LED behavior so that it is only active when the Notecard is connected to USB power.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.monitor"}
    if mode:
        req["mode"] = mode
    if count is not None:
        req["count"] = count
    if usb is not None:
        req["usb"] = usb
    return card.Transaction(req)


@validate_card_object
def motionMode(card, start=None, stop=None, seconds=None, sensitivity=None, motion=None):
    """Configure accelerometer motion monitoring parameters used when providing results to `card.motion`.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): `true` to enable the Notecard accelerometer and start motion tracking.
        stop (bool): `true` to disable the Notecard accelerometer and stop motion tracking.
        seconds (int): Period for each bucket of movements to be accumulated when `minutes` is used with `card.motion`.
        sensitivity (int): Used to set the accelerometer sample rate. The default sample rate of 1.6Hz could miss short-duration accelerations (e.g. bumps and jolts), and free fall detection may not work reliably with short falls. The penalty for increasing the sample rate to 25Hz is increased current consumption by ~1.5uA relative to the default `-1` setting.
        motion (int): If `motion` is > 0, a card.motion request will return a `"mode"` of `"moving"` or `"stopped"`. The `motion` value is the threshold for how many motion events in a single bucket will trigger a motion status change.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.motion.mode"}
    if start is not None:
        req["start"] = start
    if stop is not None:
        req["stop"] = stop
    if seconds is not None:
        req["seconds"] = seconds
    if sensitivity is not None:
        req["sensitivity"] = sensitivity
    if motion is not None:
        req["motion"] = motion
    return card.Transaction(req)


@validate_card_object
def motion(card, minutes=None):
    """Return information about the Notecard accelerometer's motion and orientation. Motion tracking must be enabled first with `card.motion.mode`. Otherwise, this request will return `{}`.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): Amount of time to sample for buckets of accelerometer-measured movement. For instance, `5` will sample motion events for the previous five minutes and return a `movements` string with motion counts in each bucket.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.motion"}
    if minutes is not None:
        req["minutes"] = minutes
    return card.Transaction(req)


@validate_card_object
def motionSync(card, start=None, stop=None, minutes=None, count=None, threshold=None):
    """Configure automatic sync triggered by Notecard movement.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): `true` to start motion-triggered syncing.
        stop (bool): `true` to stop motion-triggered syncing.
        minutes (int): The maximum frequency at which sync will be triggered. Even if a `threshold` is set and exceeded, there will only be a single sync for this amount of time.
        count (int): The number of most recent motion buckets to examine.
        threshold (int): The number of buckets that must indicate motion in order to trigger a sync. If set to `0`, the Notecard will only perform a sync when its orientation changes.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.motion.sync"}
    if start is not None:
        req["start"] = start
    if stop is not None:
        req["stop"] = stop
    if minutes is not None:
        req["minutes"] = minutes
    if count is not None:
        req["count"] = count
    if threshold is not None:
        req["threshold"] = threshold
    return card.Transaction(req)


@validate_card_object
def motionTrack(card, start=None, stop=None, minutes=None, count=None, threshold=None, file=None, now=None):
    """Configure automatic capture of Notecard accelerometer motion in a Notefile.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): `true` to start motion capture.
        stop (bool): `true` to stop motion capture.
        minutes (int): The maximum period to capture Notes in the Notefile.
        count (int): The number of most recent motion buckets to examine.
        threshold (int): The number of buckets that must indicate motion in order to capture.
        file (str): The Notefile to use for motion capture Notes. See the `_motion.qo` Notefile's documentation for details on the format of the data captured.
        now (bool): Set to `true` to trigger the immediate creation of a `_motion.qo` event if the orientation of the Notecard changes (overriding the `minutes` setting).

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.motion.track"}
    if start is not None:
        req["start"] = start
    if stop is not None:
        req["stop"] = stop
    if minutes is not None:
        req["minutes"] = minutes
    if count is not None:
        req["count"] = count
    if threshold is not None:
        req["threshold"] = threshold
    if file:
        req["file"] = file
    if now is not None:
        req["now"] = now
    return card.Transaction(req)


@validate_card_object
def random(card, mode=None, count=None):
    """Obtain a single random 32 bit unsigned integer modulo `count` or `count` bytes of random data from the Notecard hardware random number generator.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): Accepts a single value `"payload"` and, if specified, uses the `count` value to determine the number of bytes of random data to generate and return to the host.
        count (int): If the `mode` argument is excluded from the request, the Notecard uses this as an upper-limit parameter and returns a random unsigned 32 bit integer between zero and the value provided. If `"mode":"payload"` is used, this argument sets the number of random bytes of data to return in a base64-encoded buffer from the Notecard.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.random"}
    if mode:
        req["mode"] = mode
    if count is not None:
        req["count"] = count
    return card.Transaction(req)


@validate_card_object
def power(card, minutes=None, reset=None):
    """Use `card.power` API is used to configure a connected Mojo device or to manually request power consumption readings in firmware.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): How often, in minutes, Notecard should log power consumption in a `_log.qo` Note. The default value is `720` (12 hours).
        reset (bool): Set to `true` to reset the power consumption counters back to 0.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.power"}
    if minutes is not None:
        req["minutes"] = minutes
    if reset is not None:
        req["reset"] = reset
    return card.Transaction(req)


@validate_card_object
def restart(card):
    """Perform a firmware restart of the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.restart"}
    return card.Transaction(req)


@validate_card_object
def sleep(card, on=None, off=None, seconds=None, mode=None):
    """Only valid when used with Notecard WiFi v2. Allows the ESP32-based Notecard WiFi v2 to fall back to a low current draw when idle (this behavior differs from the STM32-based Notecards that have a `STOP` mode where UART and I2C may still operate). Note that the Notecard WiFi v2 will not enable a "sleep" mode while plugged in via USB. Read more in the guide on using Deep Sleep Mode on Notecard WiFi v2.

    Args:
        card (Notecard): The current Notecard object.
        on (bool): Set to `true` to enable the Notecard WiFi v2 to sleep once it is idle for >= 30 seconds.
        off (bool): Set to `true` to disable the sleep mode on the Notecard WiFi v2.
        seconds (int): The number of seconds the Notecard will wait before entering sleep mode (minimum value is 30).
        mode (str): Set to `"accel"` to wake from deep sleep on any movement detected by the onboard accelerometer. Set to `"-accel"` to reset to the default setting.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.sleep"}
    if on is not None:
        req["on"] = on
    if off is not None:
        req["off"] = off
    if seconds is not None:
        req["seconds"] = seconds
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def restore(card, delete=None, connected=None):
    """Perform a factory reset on the Notecard and restarts. Sending this request without either of the optional arguments below will only reset the Notecard's file system, thus forcing a re-sync of all Notefiles from Notehub. On Notecard LoRa there is no option to retain configuration settings, and providing `"delete": true` is required. The Notecard LoRa retains LoRaWAN configuration after factory resets.

    Args:
        card (Notecard): The current Notecard object.
        delete (bool): Set to `true` to reset most Notecard configuration settings. Note that this does not reset stored Wi-Fi credentials or the alternate I2C address (if previously set) so the Notecard can still contact the network after a reset. The Notecard will be unable to sync with Notehub until the `ProductUID` is set again.
        connected (bool): Set to `true` to reset the Notecard on Notehub. This will delete and deprovision the Notecard from Notehub the next time the Notecard connects. This also removes any Notefile templates used by this device. Conversely, if `connected` is `false` (or omitted), the Notecard's settings and data will be restored from Notehub the next time the Notecard connects to the previously used Notehub project.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.restore"}
    if delete is not None:
        req["delete"] = delete
    if connected is not None:
        req["connected"] = connected
    return card.Transaction(req)


@validate_card_object
def status(card):
    """Return general information about the Notecard's operating status.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.status"}
    return card.Transaction(req)


@validate_card_object
def temp(card, minutes=None, status=None, stop=None, sync=None):
    """Get the current temperature from the Notecard's onboard calibrated temperature sensor. When using a Notecard Cellular or Notecard Cell+WiFi, if you connect a BME280 sensor on the I2C bus the Notecard will add `temperature`, `pressure`, and `humidity` fields to the response. If you connect an ENS210 sensor on the I2C bus the Notecard will add `temperature` and `pressure` fields to the response.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): If specified, creates a templated `temp.qo` file that gathers Notecard temperature value at the specified minutes interval. When using card.aux track mode, the sensor temperature, pressure, and humidity is also included with each Note._
        status (str): Overrides `minutes` with a voltage-variable value. For example: `"usb:15;high:30;normal:60;720"`. See Voltage-Variable Sync Behavior for more information on configuring these values.
        stop (bool): If set to `true`, the Notecard will stop logging the temperature value at the interval specified with the `minutes` parameter (see above).
        sync (bool): If set to `true`, the Notecard will immediately sync any pending `_temp.qo` Notes created with the `minutes` parameter (see above).

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.temp"}
    if minutes is not None:
        req["minutes"] = minutes
    if status:
        req["status"] = status
    if stop is not None:
        req["stop"] = stop
    if sync is not None:
        req["sync"] = sync
    return card.Transaction(req)


@validate_card_object
def time(card):
    """Retrieve current date and time information in UTC. Upon power-up, the Notecard must complete a sync to Notehub in order to obtain time and location data. Before the time is obtained, this request will return `{"zone":"UTC,Unknown"}`.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.time"}
    return card.Transaction(req)


@validate_card_object
def trace(card, mode=None):
    """Enable and disable trace mode on a Notecard for debugging.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): Set to `"on"` to enable trace mode on a Notecard, or `"off"` to disable it.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.trace"}
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def transport(card, method=None, seconds=None, allow=None, umin=None):
    """Specify the connectivity protocol to prioritize on the Notecard Cell+WiFi, or when using NTN mode with Starnote and a compatible Notecard.

    Args:
        card (Notecard): The current Notecard object.
        method (str): The connectivity method to enable on the Notecard.
        seconds (int): The amount of time a Notecard will spend on any fallback transport before retrying the first transport specified in the `method`. The default is `3600` or 60 minutes.
        allow (bool): Set to `true` to allow adding Notes to non-compact Notefiles while connected over a non-terrestrial network. See Define NTN vs non-NTN Templates.
        umin (bool): Set to `true` to force a longer network transport timeout when using Wideband Notecards.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.transport"}
    if method:
        req["method"] = method
    if seconds is not None:
        req["seconds"] = seconds
    if allow is not None:
        req["allow"] = allow
    if umin is not None:
        req["umin"] = umin
    return card.Transaction(req)


@validate_card_object
def triangulate(card, mode=None, on=None, usb=None, set=None, minutes=None, text=None, time=None):
    """Enable or disables a behavior by which the Notecard gathers information about surrounding cell towers and/or Wi-Fi access points with each new Notehub session.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): The triangulation approach to use for determining the Notecard location. The following keywords can be used separately or together in a comma-delimited list, in any order. See Using Cell Tower & Wi-Fi Triangulation for more information.
        on (bool): `true` to instruct the Notecard to triangulate even if the module has not moved. Only takes effect when `set` is `true`.
        usb (bool): `true` to use perform triangulation only when the Notecard is connected to USB power. Only takes effect when `set` is `true`.
        set (bool): `true` to instruct the module to use the state of the `on` and `usb` arguments.
        minutes (int): Minimum delay, in minutes, between triangulation attempts. Use `0` for no time-based suppression.
        text (str): When using Wi-Fi triangulation, a newline-terminated list of Wi-Fi access points obtained by the external module. Format should follow the ESP32's AT+CWLAP command output.
        time (int): When passed with `text`, records the time that the Wi-Fi access point scan was performed. If not provided, Notecard time is used.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.triangulate"}
    if mode:
        req["mode"] = mode
    if on is not None:
        req["on"] = on
    if usb is not None:
        req["usb"] = usb
    if set is not None:
        req["set"] = set
    if minutes is not None:
        req["minutes"] = minutes
    if text:
        req["text"] = text
    if time is not None:
        req["time"] = time
    return card.Transaction(req)


@validate_card_object
def usageGet(card, mode=None, offset=None):
    """Return the card's network usage statistics.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): The time period to use for statistics. Must be one of:
        offset (int): The number of time periods to look backwards, based on the specified `mode`. To accurately determine the start of the calculated time period when using `offset`, use the `time` value of the response. Likewise, to calculate the end of the time period, add the `seconds` value to the `time` value.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.usage.get"}
    if mode:
        req["mode"] = mode
    if offset is not None:
        req["offset"] = offset
    return card.Transaction(req)


@validate_card_object
def usageTest(card, days=None, hours=None, megabytes=None):
    """Calculate a projection of how long the available data quota will last based on the observed usage patterns.

    Args:
        card (Notecard): The current Notecard object.
        days (int): Number of days to use for the test.
        hours (int): If you want to analyze a period shorter than one day, the number of hours to use for the test.
        megabytes (int): The Notecard lifetime data quota (in megabytes) to use for the test.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.usage.test"}
    if days is not None:
        req["days"] = days
    if hours is not None:
        req["hours"] = hours
    if megabytes is not None:
        req["megabytes"] = megabytes
    return card.Transaction(req)


@validate_card_object
def version(card, api=None):
    """Return firmware version information for the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        api (int): Specify a major version of the Notecard firmware that a host expects to use.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.version"}
    if api is not None:
        req["api"] = api
    return card.Transaction(req)


@validate_card_object
def voltage(card, hours=None, mode=None, offset=None, vmax=None, vmin=None, name=None, usb=None, alert=None, sync=None, calibration=None, set=None):
    """Provide the current V+ voltage level on the Notecard, and provides information about historical voltage trends. When used with the mode argument, configures voltage thresholds based on how the device is powered.

    Args:
        card (Notecard): The current Notecard object.
        hours (int): The number of hours to analyze, up to 720 (30 days).
        mode (str): Used to set voltage thresholds based on how the Notecard will be powered. NOTE: Setting voltage thresholds is not supported on the Notecard XP.
        offset (int): Number of hours to move into the past before starting analysis.
        vmax (float): Ignore voltage readings above this level when performing calculations.
        vmin (float): Ignore voltage readings below this level when performing calculations.
        name (str): Specifies an environment variable to override application default timing values.
        usb (bool): When enabled, the Notecard will monitor for changes to USB power state.
        alert (bool): When enabled and the `usb` argument is set to `true`, the Notecard will add an entry to the `health.qo` Notefile when USB power is connected or disconnected.
        sync (bool): When enabled and the `usb` argument is set to `true`, the Notecard will perform a sync when USB power is connected or disconnected.
        calibration (float): The offset, in volts, to account for the forward voltage drop of the diode used between the battery and Notecard in either Blues- or customer-designed Notecarriers.
        set (bool): Used along with `calibration`, set to `true` to specify a new calibration value.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.voltage"}
    if hours is not None:
        req["hours"] = hours
    if mode:
        req["mode"] = mode
    if offset is not None:
        req["offset"] = offset
    if vmax is not None:
        req["vmax"] = vmax
    if vmin is not None:
        req["vmin"] = vmin
    if name:
        req["name"] = name
    if usb is not None:
        req["usb"] = usb
    if alert is not None:
        req["alert"] = alert
    if sync is not None:
        req["sync"] = sync
    if calibration is not None:
        req["calibration"] = calibration
    if set is not None:
        req["set"] = set
    return card.Transaction(req)


@validate_card_object
def wirelessPenalty(card, reset=None, set=None, rate=None, add=None, max=None, min=None):
    """View the current state of a Notecard Penalty Box, manually remove the Notecard from a penalty box, or override penalty box defaults.

    Args:
        card (Notecard): The current Notecard object.
        reset (bool): Set to `true` to remove the Notecard from certain types of penalty boxes.
        set (bool): Set to `true` to override the default settings of the Network Registration Failure Penalty Box.
        rate (float): The rate at which the penalty box time multiplier is increased over successive retries. Used with the `set` argument to override the Network Registration Failure Penalty Box defaults.
        add (int): The number of minutes to add to successive retries. Used with the `set` argument to override the Network Registration Failure Penalty Box defaults.
        max (int): The maximum number of minutes that a device can be in a Network Registration Failure Penalty Box. Used with the `set` argument to override the Network Registration Failure Penalty Box defaults.
        min (int): The number of minutes of the first retry interval of a Network Registration Failure Penalty Box. Used with the `set` argument to override the Network Registration Failure Penalty Box defaults.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.wireless.penalty"}
    if reset is not None:
        req["reset"] = reset
    if set is not None:
        req["set"] = set
    if rate is not None:
        req["rate"] = rate
    if add is not None:
        req["add"] = add
    if max is not None:
        req["max"] = max
    if min is not None:
        req["min"] = min
    return card.Transaction(req)


@validate_card_object
def wireless(card, mode=None, apn=None, method=None, hours=None):
    """View the last known network state, or customize the behavior of the modem. Note: Be careful when using this mode with hardware not on hand as a mistake may cause loss of network and Notehub access.

    Args:
        card (Notecard): The current Notecard object.
        mode (str): Network scan mode. Must be one of:
        apn (str): Access Point Name (APN) when using an external SIM. Use `"-"` to reset to the Notecard default APN.
        method (str): Used when configuring a Notecard to failover to a different SIM.
        hours (int): When using the `method` argument with `"dual-primary-secondary"` or `"dual-secondary-primary"`, this is the number of hours after which the Notecard will attempt to switch back to the preferred SIM.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.wireless"}
    if mode:
        req["mode"] = mode
    if apn:
        req["apn"] = apn
    if method:
        req["method"] = method
    if hours is not None:
        req["hours"] = hours
    return card.Transaction(req)


@validate_card_object
def wifi(card, ssid=None, password=None, name=None, org=None, start=None, text=None):
    r"""Set up a Notecard WiFi to connect to a Wi-Fi access point.

    Args:
        card (Notecard): The current Notecard object.
        ssid (str): The SSID of the Wi-Fi access point. Alternatively, use `-` to clear an already set SSID.
        password (str): The network password of the Wi-Fi access point. Alternatively, use `-` to clear an already set password or to connect to an open access point.
        name (str): By default, the Notecard creates a SoftAP (software enabled access point) under the name "Notecard". You can use the `name` argument to change the name of the SoftAP to a custom name. If you include a `-` at the end of the `name` (for example `"name": "acme-"`), the Notecard will append the last four digits of the network's MAC address (for example `acme-025c`). This allows you to distinguish between multiple Notecards in SoftAP mode.
        org (str): If specified, replaces the Blues logo on the SoftAP page with the provided name.
        start (bool): Specify `true` to activate SoftAP mode on the Notecard programmatically.
        text (str): A string containing an array of access points the Notecard should attempt to use. The access points should be provided in the following format: `["FIRST-SSID","FIRST-PASSWORD"],["SECOND-SSID","SECOND-PASSWORD"]`. You may need to escape any quotes used in this argument before passing it to the Notecard. For example, the following is a valid request to pass to a Notecard through the In-Browser Terminal. `{"req":"card.wifi", "text":"[\"FIRST-SSID\",\"FIRST-PASSWORD\"]"}`

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.wifi"}
    if ssid:
        req["ssid"] = ssid
    if password:
        req["password"] = password
    if name:
        req["name"] = name
    if org:
        req["org"] = org
    if start is not None:
        req["start"] = start
    if text:
        req["text"] = text
    return card.Transaction(req)
