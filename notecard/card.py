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
def attn(card, mode=None, files=None, seconds=None, payload=None, start=None):
    """Configure interrupt detection between a host and Notecard.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The attn mode to set.
        files (array): A collection of notefiles to watch.
        seconds (int): A timeout to use when arming attn mode.
        payload (int): When using sleep mode, a payload of data from the host
            that the Notecard should hold in memory until retrieved by
            the host.
        start (bool): When using sleep mode and the host has reawakened,
            request the Notecard to return the stored payload.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.attn"}
    if mode:
        req["mode"] = mode
    if files:
        req["files"] = files
    if seconds:
        req["seconds"] = seconds
    if payload:
        req["payload"] = payload
    if start:
        req["start"] = start
    return card.Transaction(req)


@validate_card_object
def time(card):
    """Retrieve the current time and date from the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.time"}
    return card.Transaction(req)


@validate_card_object
def status(card):
    """Retrieve the status of the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.status"}
    return card.Transaction(req)


@validate_card_object
def temp(card, minutes=None):
    """Retrieve the current temperature from the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): If specified, creates a templated _temp.qo file that
            gathers Notecard temperature value at the specified interval.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.temp"}
    if minutes:
        req["minutes"] = minutes
    return card.Transaction(req)


@validate_card_object
def version(card):
    """Retrieve firmware version information from the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.version"}
    return card.Transaction(req)


@validate_card_object
def voltage(card, hours=None, offset=None, vmax=None, vmin=None):
    """Retrieve current and historical voltage info from the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        hours (int): Number of hours to analyze.
        offset (int): Number of hours to offset.
        vmax (decimal): max voltage level to report.
        vmin (decimal): min voltage level to report.

    Returns:
        string: The result of the Notecard request.
    """
    req = {"req": "card.voltage"}
    if hours:
        req["hours"] = hours
    if offset:
        req["offset"] = offset
    if vmax:
        req["vmax"] = vmax
    if vmin:
        req["vmin"] = vmin
    return card.Transaction(req)


@validate_card_object
def wireless(card, mode=None, apn=None):
    """Retrieve wireless modem info or customize modem behavior.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The wireless module mode to set. Must be one of:
            "-" to reset to the default mode
            "auto" to perform automatic band scan mode (default)
            "m" to restrict the modem to Cat-M1
            "nb" to restrict the modem to Cat-NB1
            "gprs" to restrict the modem to EGPRS
        apn (string): Access Point Name (APN) when using an external SIM.
            Use "-" to reset to the Notecard default APN.

    Returns:
        dict: The result of the Notecard request containing network status and
        signal information.
    """
    req = {"req": "card.wireless"}
    if mode:
        req["mode"] = mode
    if apn:
        req["apn"] = apn
    return card.Transaction(req)


@validate_card_object
def transport(card, method=None, allow=None):
    """Configure the Notecard's connectivity method.

    Args:
        card (Notecard): The current Notecard object.
        method (string): The connectivity method to enable. Must be one of:
            "-" to reset to device default
            "wifi-cell" to prioritize WiFi with cellular fallback
            "wifi" to enable WiFi only
            "cell" to enable cellular only
            "ntn" to enable Non-Terrestrial Network mode
            "wifi-ntn" to prioritize WiFi with NTN fallback
            "cell-ntn" to prioritize cellular with NTN fallback
            "wifi-cell-ntn" to prioritize WiFi, then cellular, then NTN
        allow (bool): When True, allows adding Notes to non-compact Notefiles
            while connected over a non-terrestrial network.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.transport"}
    if method:
        req["method"] = method
    if allow is not None:
        req["allow"] = allow
    return card.Transaction(req)


@validate_card_object
def power(card, minutes=None, reset=None):
    """Configure a connected Mojo device or request power consumption readings in firmware.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): The number of minutes to log power consumption. Default is 720 minutes (12 hours).
        reset (bool): When True, resets the power consumption counter back to 0.

    Returns:
        dict: The result of the Notecard request. The response will contain the following fields:
            "voltage": The current voltage.
            "milliamp_hours": The cumulative energy consumption in milliamp hours.
            "temperature": The Notecard's internal temperature in degrees centigrade, including offset.
    """
    req = {"req": "card.power"}
    if minutes:
        req["minutes"] = minutes
    if reset:
        req["reset"] = reset
    return card.Transaction(req)


@validate_card_object
def location(card):
    """Retrieve the last known location of the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request containing location information including:
            "status": The current status of the Notecard GPS/GNSS connection
            "mode": The GPS/GNSS connection mode (continuous, periodic, or off)
            "lat": The latitude in degrees of the last known location
            "lon": The longitude in degrees of the last known location
            "time": UNIX Epoch time of location capture
            "max": If a geofence is enabled by card.location.mode, meters from the geofence center
            "count": The number of consecutive recorded GPS/GNSS failures
            "dop": The "Dilution of Precision" value from the latest GPS/GNSS reading
    """
    req = {"req": "card.location"}
    return card.Transaction(req)


@validate_card_object
def locationMode(card, mode=None, seconds=None, vseconds=None, lat=None, lon=None, max=None):
    """Set location-related configuration settings.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The location mode to set. Must be one of:
            - "" (empty string) to retrieve the current mode
            - "off" to turn location mode off
            - "periodic" to sample location at a specified interval
            - "continuous" to enable the Notecard's GPS/GNSS module for continuous sampling
            - "fixed" to report the location as a fixed location
        seconds (int): When in periodic mode, location will be sampled at this interval, if the Notecard detects motion.
        vseconds (string): In periodic mode, overrides seconds with a voltage-variable value.
        lat (float): Used with fixed mode to specify the latitude coordinate.
        lon (float): Used with fixed mode to specify the longitude coordinate.
        max (int): Maximum number of seconds to wait for a GPS fix.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.location.mode"}
    if mode is not None:
        req["mode"] = mode
    if seconds:
        req["seconds"] = seconds
    if vseconds:
        req["vseconds"] = vseconds
    if lat is not None:
        req["lat"] = lat
    if lon is not None:
        req["lon"] = lon
    if max:
        req["max"] = max
    return card.Transaction(req)


@validate_card_object
def locationTrack(card, start=None, heartbeat=None, hours=None, sync=None, stop=None, file=None):
    """Store location data in a Notefile at the periodic interval, or using a specified heartbeat.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): Set to True to start Notefile tracking.
        heartbeat (bool): When start is True, set to True to enable tracking even when motion is not detected.
        hours (int): If heartbeat is True, add a heartbeat entry at this hourly interval.
                    Use a negative integer to specify a heartbeat in minutes instead of hours.
        sync (bool): Set to True to perform an immediate sync to the Notehub each time a new Note is added.
        stop (bool): Set to True to stop Notefile tracking.
        file (string): The name of the Notefile to store location data in. Defaults to "track.qo".

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.location.track"}
    if start is not None:
        req["start"] = start
    if heartbeat is not None:
        req["heartbeat"] = heartbeat
    if hours:
        req["hours"] = hours
    if sync is not None:
        req["sync"] = sync
    if stop is not None:
        req["stop"] = stop
    if file:
        req["file"] = file
    return card.Transaction(req)


@validate_card_object
def binary(card, delete=None):
    """View the status of the binary storage area of the Notecard and optionally clear data.

    Args:
        card (Notecard): The current Notecard object.
        delete (bool): Set to True to clear the COBS area on the Notecard and reset all related arguments.

    Returns:
        dict: The result of the Notecard request containing binary storage information including:
            "cobs": The size of COBS-encoded data stored in the reserved area
            "connected": Returns True if the Notecard is connected to the network
            "err": If present, a string describing the error that occurred during transmission
            "length": The length of the binary data
            "max": Available storage space
            "status": MD5 checksum of unencoded buffer
    """
    req = {"req": "card.binary"}
    if delete is not None:
        req["delete"] = delete
    return card.Transaction(req)


@validate_card_object
def binaryGet(card, cobs=None, offset=None, length=None):
    """Retrieve binary data stored in the binary storage area of the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        cobs (int): The size of the COBS-encoded data you are expecting to be returned (in bytes).
        offset (int): Used along with length, the number of bytes to offset the binary payload from 0 when retrieving binary data.
        length (int): Used along with offset, the number of bytes to retrieve from the binary storage area.

    Returns:
        dict: The result of the Notecard request. The response returns the JSON-formatted response object, then the binary data.
            "status": The MD5 checksum of the data returned, after it has been decoded
            "err": If present, a string describing the error that occurred during transmission
    """
    req = {"req": "card.binary.get"}
    if cobs:
        req["cobs"] = cobs
    if offset is not None:
        req["offset"] = offset
    if length:
        req["length"] = length
    return card.Transaction(req)


@validate_card_object
def binaryPut(card, offset=None, cobs=None, status=None):
    """Add binary data to the binary storage area of the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        offset (int): The number of bytes to offset the binary payload from 0 when appending the binary data to the binary storage area.
        cobs (int): The size of the COBS-encoded data (in bytes).
        status (string): The MD5 checksum of the data, before it has been encoded.

    Returns:
        dict: The result of the Notecard request. The Notecard expects to receive binary data immediately following the usage of this API command.
            "err": If present, a string describing the error that occurred during transmission
    """
    req = {"req": "card.binary.put"}
    if offset is not None:
        req["offset"] = offset
    if cobs:
        req["cobs"] = cobs
    if status:
        req["status"] = status
    return card.Transaction(req)


@validate_card_object
def carrier(card, mode=None):
    """Configure the AUX_CHARGING pin to notify the Notecard about charging support on a Notecarrier.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The AUX_CHARGING mode. Set to "charging" to tell the Notecard that AUX_CHARGING
                      is connected to a Notecarrier that supports charging. Set to "-" or "off" to turn off
                      the AUX_CHARGING detection.

    Returns:
        dict: The result of the Notecard request containing:
            "mode": The current AUX_CHARGING mode, or "off" if not set
            "charging": Will display True when in AUX_CHARGING "charging" mode
    """
    req = {"req": "card.carrier"}
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def contact(card, name=None, org=None, role=None, email=None):
    """Set or retrieve information about the Notecard maintainer.

    Args:
        card (Notecard): The current Notecard object.
        name (string): Set the name of the Notecard maintainer.
        org (string): Set the organization name of the Notecard maintainer.
        role (string): Set the role of the Notecard maintainer.
        email (string): Set the email address of the Notecard maintainer.

    Returns:
        dict: The result of the Notecard request containing:
            "name": Name of the Notecard maintainer
            "org": Organization name of the Notecard maintainer
            "role": Role of the Notecard maintainer
            "email": Email address of the Notecard maintainer
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
def aux(card, mode=None, usage=None, seconds=None, max=None, start=None, gps=None,
        rate=None, sync=None, file=None, connected=None, limit=None, sensitivity=None,
        ms=None, count=None, offset=None):
    """Configure various uses of the general-purpose I/O (GPIO) pins AUX1-AUX4 for tracking and sensing tasks.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The AUX mode. Options include: "dfu", "gpio", "led", "monitor", "motion",
                      "neo", "neo-monitor", "off", "track", "track-monitor", "track-neo-monitor".
        usage (array): An ordered list of pin modes for each AUX pin when in GPIO mode.
        seconds (int): When in gpio mode, if an AUX pin is configured as a count type,
                      the count of rising edges can be broken into samples of this duration.
        max (int): When in gpio mode, if an AUX pin is configured as a count type,
                  the maximum number of samples of duration seconds.
        start (bool): When in gpio mode, if an AUX pin is configured as a count type,
                     set to True to reset counters and start incrementing.
        gps (bool): Deprecated. If True, along with mode:track the Notecard supports
                   the use of an external GPS module.
        rate (int): The AUX UART baud rate for debug communication over the AUXRX and AUXTX pins.
        sync (bool): If True, for pins set as input by usage, the Notecard will autonomously
                    report any state changes as new notes in file.
        file (string): The name of the Notefile used to report state changes when used
                      in conjunction with sync:True.
        connected (bool): If True, defers the sync of the state change Notefile to the next
                         sync as configured by the hub.set request.
        limit (bool): If True, along with mode:track and gps:True the Notecard will disable
                     concurrent modem use during GPS tracking.
        sensitivity (int): When used with mode:neo-monitor or mode:track-neo-monitor,
                          this controls the brightness of NeoPixel lights.
        ms (int): When in gpio mode, this argument configures a debouncing interval.
        count (int): When used with mode:neo-monitor or mode:track-neo-monitor,
                    this controls the number of NeoPixels to use in a strip.
        offset (int): When used with mode:neo-monitor or mode:track-neo-monitor,
                     this is the 1-based index in a strip of NeoPixels.

    Returns:
        dict: The result of the Notecard request containing:
            "mode": The current mode of the AUX interface
            "text": Text received over the AUX interface
            "binary": Binary data received over the AUX interface
            "count": Number of bytes received
    """
    req = {"req": "card.aux"}
    if mode:
        req["mode"] = mode
    if usage:
        req["usage"] = usage
    if seconds:
        req["seconds"] = seconds
    if max:
        req["max"] = max
    if start is not None:
        req["start"] = start
    if gps is not None:
        req["gps"] = gps
    if rate:
        req["rate"] = rate
    if sync is not None:
        req["sync"] = sync
    if file:
        req["file"] = file
    if connected is not None:
        req["connected"] = connected
    if limit is not None:
        req["limit"] = limit
    if sensitivity:
        req["sensitivity"] = sensitivity
    if ms:
        req["ms"] = ms
    if count:
        req["count"] = count
    if offset:
        req["offset"] = offset
    return card.Transaction(req)


@validate_card_object
def auxSerial(card, mode=None, duration=None, rate=None, limit=None, max=None, ms=None, minutes=None):
    """Configure various uses of the AUXTX and AUXRX pins on the Notecard's edge connector.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The AUX mode. Must be one of the following:
                      "req" - Request/response monitoring (default)
                      "gps" - Use external GPS/GNSS module
                      "notify" - Stream data or notifications
                      "notify,accel" - Stream accelerometer readings
                      "notify,signals" - Notify of Inbound Signals
                      "notify,env" - Notify of Environment Variable changes
                      "notify,dfu" - Notify of DFU events
        duration (int): For mode "accel", specify sampling duration for accelerometer.
        rate (int): Baud rate for transmission (default 115200, 9600 for GPS).
        limit (bool): Disable concurrent modem use during GPS tracking.
        max (int): Maximum data to send per session in bytes.
        ms (int): Delay in milliseconds before sending buffer.
        minutes (int): Interval for notifying host when using mode "dfu".

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "card.aux.serial"}
    if mode:
        req["mode"] = mode
    if duration:
        req["duration"] = duration
    if rate:
        req["rate"] = rate
    if limit is not None:
        req["limit"] = limit
    if max:
        req["max"] = max
    if ms:
        req["ms"] = ms
    if minutes:
        req["minutes"] = minutes
    return card.Transaction(req)


@validate_card_object
def dfu(card, name=None, on=None, off=None, seconds=None, stop=None, start=None, mode=None):
    """Configure a Notecard for Notecard Outboard Firmware Update.

    Args:
        card (Notecard): The current Notecard object.
        name (string): One of the supported classes of host MCU. Supported MCU classes are
                      'esp32', 'stm32', 'stm32-bi', 'mcuboot', '-'.
        on (bool): Set to True to enable Notecard Outboard Firmware Update.
        off (bool): Set to True to disable Notecard Outboard Firmware Update from occurring.
        seconds (int): When used with 'off':True, disable Notecard Outboard Firmware Update
                      operations for the specified number of seconds.
        stop (bool): Set to True to disable the host RESET that is normally performed on the
                    host MCU when the Notecard starts up.
        start (bool): Set to True to enable the host RESET.
        mode (string): Optional mode for alternative DFU configuration.

    Returns:
        dict: The result of the Notecard request containing:
            "name": Current MCU class configured for DFU
    """
    req = {"req": "card.dfu"}
    if name:
        req["name"] = name
    if on is not None:
        req["on"] = on
    if off is not None:
        req["off"] = off
    if seconds:
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
    """Retrieve an illumination reading from an OPT3001 ambient light sensor connected to Notecard's I2C bus.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request containing:
            "value": An illumination reading (in lux) from the attached OPT3001 sensor.

    Note:
        If no OPT3001 sensor is detected, this request returns an "illumination sensor is not available" error.
    """
    req = {"req": "card.illumination"}
    return card.Transaction(req)


@validate_card_object
def io(card, i2c=None, mode=None):
    """Override the Notecard's I2C address and change behaviors of the onboard LED and USB port.

    Args:
        card (Notecard): The current Notecard object.
        i2c (int): The alternate address to use for I2C communication. Pass -1 to reset to the default address.
        mode (string): Mode to change LED or USB behavior. Options include:
                      "-usb" - Disable the Notecard's USB port. Re-enable with "usb" or "+usb"
                      "+busy" - LED will be on when Notecard is awake, off when asleep
                      "-busy" - Reset "+busy" to default (LED blinks only during flash operations)
                      "i2c-master-disable" - Disable Notecard acting as an I2C master
                      "i2c-master-enable" - Re-enable I2C master functionality

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
    """Control connected LEDs or manage a single connected NeoPixel.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): Used to specify the color of the LED or NeoPixel to control.
                      For LEDs: 'red', 'green', 'yellow'
                      For NeoPixels: 'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'orange', 'white', 'gray'
        on (bool): Set to True to turn the specified LED or NeoPixel on.
        off (bool): Set to True to turn the specified LED or NeoPixel off.

    Returns:
        dict: The result of the Notecard request.

    Note:
        Requires the card.aux API to be configured in 'led' or 'neo' mode first.
        Not supported by Notecard LoRa for regular LEDs.
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
def monitor(card, mode=None, count=None, usb=None):
    """Configure AUX pins when in monitor mode.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): Set LED color. Options: 'green', 'red', 'yellow'.
        count (int): Number of pulses to send to AUX pin LED. Set this to 0 to return to default LED behavior.
        usb (bool): Set to true to configure LED behavior so that it is only active when the Notecard is connected to USB power.

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
def motion(card, minutes=None):
    """Retrieve information about the Notecard's accelerometer motion and orientation.

    Args:
        card (Notecard): The current Notecard object.
        minutes (int): Amount of time to sample for buckets of accelerometer-measured movement.

    Returns:
        dict: The result of the Notecard request containing:
            "count": Number of accelerometer motion events since the last card.motion request
            "alert": Boolean indicating free-fall detection since the last request
            "motion": UNIX Epoch time of the last accelerometer motion event
            "status": Comma-separated list of orientation events (e.g., "face-up", "portrait-down")
            "seconds": Duration of each bucket of sample accelerometer movements (when minutes is provided)
            "movements": Base-36 characters representing motion counts in each bucket
            "mode": Current motion status of the Notecard (e.g., "stopped" or "moving")
    """
    req = {"req": "card.motion"}
    if minutes is not None:
        req["minutes"] = minutes
    return card.Transaction(req)


@validate_card_object
def motionMode(card, start=None, stop=None, seconds=None, sensitivity=None, motion=None):
    """Configure accelerometer motion monitoring parameters.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): Set to True to enable the Notecard accelerometer and start motion tracking.
        stop (bool): Set to True to disable the Notecard accelerometer and stop motion tracking.
        seconds (int): Period for each bucket of movements to be accumulated when minutes is used with card.motion.
        sensitivity (int): Sets accelerometer sample rate with different sensitivity levels (default -1).
        motion (int): Threshold for motion events to trigger motion status change between "moving" and "stopped".

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
def motionSync(card, start=None, stop=None, minutes=None, count=None, threshold=None):
    """Configure automatic sync triggered by Notecard movement.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): Set to True to start motion-triggered syncing.
        stop (bool): Set to True to stop motion-triggered syncing.
        minutes (int): Maximum frequency at which sync will be triggered.
        count (int): Number of most recent motion buckets to examine.
        threshold (int): Number of buckets that must indicate motion to trigger a sync.
                        If set to 0, sync occurs only on orientation changes.

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
    """Configure automatic capture of accelerometer motion in a Notefile.

    Args:
        card (Notecard): The current Notecard object.
        start (bool): Set to True to start motion capture.
        stop (bool): Set to True to stop motion capture.
        minutes (int): Maximum period to capture Notes in the Notefile.
        count (int): Number of most recent motion buckets to examine.
        threshold (int): Number of buckets that must indicate motion to capture.
        file (string): Notefile to use for motion capture Notes (default '_motion.qo').
        now (bool): Set to True to trigger immediate _motion.qo event on orientation change.

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
    if file is not None:
        req["file"] = file
    if now is not None:
        req["now"] = now
    return card.Transaction(req)


@validate_card_object
def restart(card):
    """Perform a firmware restart of the Notecard.

    Args:
        card (Notecard): The current Notecard object.

    Returns:
        dict: The result of the Notecard request.

    Warning:
        Not recommended for production applications due to potential increased
        cellular data and consumption credit usage.
    """
    req = {"req": "card.restart"}
    return card.Transaction(req)


@validate_card_object
def restore(card, delete=None, connected=None):
    """Reset Notecard configuration settings and/or deprovision from Notehub.

    Args:
        card (Notecard): The current Notecard object.
        delete (bool): Set to True to reset most Notecard configuration settings.
                      Does not reset Wi-Fi credentials or alternate I2C address.
                      Notecard will be unable to sync with Notehub until ProductUID is set again.
                      On Notecard LoRa, this parameter is required, though LoRaWAN configuration is retained.
        connected (bool): Set to True to reset the Notecard on Notehub.
                         Will delete and deprovision the Notecard from Notehub on next connection.
                         Removes any Notefile templates used by the device.

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
def sleep(card, on=None, off=None, seconds=None, mode=None):
    """Configure sleep mode for Notecard WiFi v2.

    Args:
        card (Notecard): The current Notecard object.
        on (bool): Set to True to enable sleep mode after 30 seconds of idleness.
        off (bool): Set to True to disable sleep mode.
        seconds (int): Number of seconds before entering sleep mode (minimum 30).
        mode (string): Accelerometer wake configuration.
                      Use "accel" to wake from deep sleep on accelerometer movement,
                      or "-accel" to reset to default setting.

    Returns:
        dict: The result of the Notecard request containing:
            "on": Boolean indicating if sleep mode is enabled
            "off": Boolean indicating if sleep mode is disabled
            "seconds": Configured sleep delay
            "mode": Accelerometer wake configuration

    Note:
        Only valid for Notecard WiFi v2.
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
def trace(card, mode=None):
    """Enable and disable trace mode on a Notecard for debugging.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): Set to "on" to enable trace mode on a Notecard, or "off" to disable it.

    Returns:
        dict: The result of the Notecard request.

    Note:
        See: https://dev.blues.io/guides-and-tutorials/notecard-guides/using-notecard-trace-mode
    """
    req = {"req": "card.trace"}
    if mode:
        req["mode"] = mode
    return card.Transaction(req)


@validate_card_object
def triangulate(card, mode=None, on=None, usb=None, set=None, minutes=None, text=None, time=None):
    """Enable or disable triangulation behavior for gathering cell tower and Wi-Fi access point information.

    Args:
        card (Notecard): The current Notecard object.
        mode (string): The triangulation approach to use. Keywords can be used separately or together
                      in a comma-delimited list: "cell", "wifi", or "-" to clear the mode.
        on (bool): Set to True to triangulate even if the module has not moved.
                  Only takes effect when set is True. Default: False.
        usb (bool): Set to True to perform triangulation only when connected to USB power.
                   Only takes effect when set is True. Default: False.
        set (bool): Set to True to instruct the module to use the state of the on and usb arguments.
                   Default: False.
        minutes (int): Minimum delay, in minutes, between triangulation attempts.
                      Use 0 for no time-based suppression. Default: 0.
        text (string): When using Wi-Fi triangulation, a newline-terminated list of Wi-Fi access points.
                      Format should follow ESP32's AT+CWLAP command output.
        time (int): UNIX Epoch time when the Wi-Fi access point scan was performed.
                   If not provided, Notecard time is used.

    Returns:
        dict: The result of the Notecard request containing:
            "motion": UNIX Epoch time of last detected Notecard movement
            "time": UNIX Epoch time of last triangulation scan
            "mode": Comma-separated list indicating active triangulation modes
            "on": Boolean if triangulation scans will be performed even if device has not moved
            "usb": Boolean if triangulation scans will be performed only when USB-powered
            "length": Length of the text buffer provided in current or previous request

    Note:
        See: https://dev.blues.io/notecard/notecard-walkthrough/time-and-location-requests/#using-cell-tower-and-wi-fi-triangulation
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
        mode (string): The time period to use for statistics. Must be one of:
                      "total" for all stats since activation (default),
                      "1hour", "1day", "30day".
        offset (int): The number of time periods to look backwards, based on the specified mode.

    Returns:
        dict: The result of the Notecard request containing:
            "seconds": Number of seconds in the analyzed period
            "time": UNIX Epoch time of start of analyzed period (or activation time if mode="total")
            "bytes_sent": Number of bytes sent by the Notecard to Notehub
            "bytes_received": Number of bytes received by the Notecard from Notehub
            "notes_sent": Approximate number of notes sent by the Notecard to Notehub
            "notes_received": Approximate number of notes received by the Notecard from Notehub
            "sessions_standard": Number of standard Notehub sessions
            "sessions_secure": Number of secure Notehub sessions

    Note:
        Usage data is updated at the end of each network connection. If connected in continuous mode,
        usage data will not be updated until the current session ends.
        See: https://dev.blues.io/notecard/notecard-walkthrough/low-bandwidth-design#measuring-data-usage
    """
    req = {"req": "card.usage.get"}
    if mode:
        req["mode"] = mode
    if offset is not None:
        req["offset"] = offset
    return card.Transaction(req)


@validate_card_object
def usageTest(card, days=None, hours=None, megabytes=None):
    """Test and project data usage based on historical usage patterns.

    Args:
        card (Notecard): The current Notecard object.
        days (int): Number of days to use for the test.
        hours (int): If analyzing a period shorter than one day, the number of hours to use for the test.
        megabytes (int): The Notecard lifetime data quota (in megabytes) to use for the test. Default: 1024.

    Returns:
        dict: The result of the Notecard request containing:
            "max": Days of projected data available based on test
            "days": Number of days used for the test
            "bytes_per_day": Average bytes per day used during the test period
            "seconds": Number of seconds in the analyzed period
            "time": UNIX Epoch time of device activation
            "bytes_sent": Number of bytes sent by the Notecard to Notehub
            "bytes_received": Number of bytes received by the Notecard from Notehub
            "notes_sent": Number of notes sent by the Notecard to Notehub
            "notes_received": Number of notes received by the Notecard from Notehub
            "sessions_standard": Number of standard Notehub sessions
            "sessions_secure": Number of secure Notehub sessions

    Note:
        See: https://dev.blues.io/notecard/notecard-walkthrough/low-bandwidth-design#projecting-the-lifetime-of-available-data
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
def wifi(card, ssid=None, password=None, name=None, org=None, start=None, text=None):
    """Set up a Notecard WiFi to connect to a Wi-Fi access point.

    Args:
        card (Notecard): The current Notecard object.
        ssid (string): The SSID of the Wi-Fi access point. Use "-" to clear an already set SSID.
        password (string): The network password of the Wi-Fi access point.
                          Use "-" to clear an already set password or to connect to an open access point.
        name (string): Custom name for the SoftAP (software enabled access point).
                      Default is "Notecard". Use "-" suffix to append MAC address digits.
        org (string): If specified, replaces the Blues logo on the SoftAP page with the provided name.
        start (bool): Set to True to activate SoftAP mode on the Notecard programmatically.
        text (string): String containing an array of access points in format:
                      '["FIRST-SSID","FIRST-PASSWORD"],["SECOND-SSID","SECOND-PASSWORD"]'

    Returns:
        dict: The result of the Notecard request containing:
            "secure": Boolean indicating if Wi-Fi access point uses Management Frame Protection
            "version": Silicon Labs WF200 Wi-Fi Transceiver binary version
            "ssid": SSID of the Wi-Fi access point
            "security": Security protocol the Wi-Fi access point uses

    Note:
        Updates to WiFi credentials cannot occur while Notecard is in continuous mode.
        Change to periodic or off mode first using hub.set.
        See: https://dev.blues.io/guides-and-tutorials/notecard-guides/connecting-to-a-wi-fi-access-point/
    """
    req = {"req": "card.wifi"}
    if ssid:
        req["ssid"] = ssid
    if password is not None:
        req["password"] = password
    if name:
        req["name"] = name
    if org is not None:
        req["org"] = org
    if start is not None:
        req["start"] = start
    if text:
        req["text"] = text
    return card.Transaction(req)


@validate_card_object
def wirelessPenalty(card, reset=None, set=None, rate=None, add=None, max=None, min=None):
    """View the current state of a Notecard Penalty Box, manually remove from penalty box, or override defaults.

    Args:
        card (Notecard): The current Notecard object.
        reset (bool): Set to True to remove the Notecard from certain types of penalty boxes.
        set (bool): Set to True to override the default settings of the Network Registration Failure Penalty Box.
        rate (float): The rate at which the penalty box time multiplier is increased over successive retries.
                     Default: 1.25. Used with set argument.
        add (int): The number of minutes to add to successive retries. Default: 15. Used with set argument.
        max (int): The maximum number of minutes that a device can be in a Network Registration Failure
                  Penalty Box. Default: 4320. Used with set argument.
        min (int): The number of minutes of the first retry interval of a Network Registration Failure
                  Penalty Box. Default: 15. Used with set argument.

    Returns:
        dict: The result of the Notecard request containing:
            "minutes": Time since the first network registration failure
            "count": Number of consecutive network registration failures
            "status": If in a Penalty Box, provides associated Error and Status Codes
            "seconds": If in a Penalty Box, number of seconds until the penalty condition ends

    Warning:
        Misuse of this feature may result in the cellular carrier preventing future connections
        or blacklisting devices for attempting to connect too frequently.

    Note:
        See: https://dev.blues.io/guides-and-tutorials/notecard-guides/understanding-notecard-penalty-boxes
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
