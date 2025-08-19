"""web Fluent API Helper."""

##
# @file web.py
#
# @brief web Fluent API Helper.
#
# @section description Description
# This module contains helper methods for calling web.* Notecard API commands.
# This module is optional and not required for use with the Notecard.

from notecard.validators import validate_card_object


@validate_card_object
def delete(card, route=None, name=None, content=None, seconds=None, async_=None, file=None, note=None):
    """Perform a simple HTTP or HTTPS `DELETE` request against an external endpoint, and returns the response to the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        route (str): Alias for a Proxy Route in Notehub.
        name (str): A web URL endpoint relative to the host configured in the Proxy Route. URL parameters may be added to this argument as well (e.g. `/deleteReading?id=1`).
        content (str): The MIME type of the body or payload of the response. Default is `application/json`.
        seconds (int): If specified, overrides the default 90 second timeout.
        async_ (bool): If `true`, the Notecard performs the web request asynchronously, and returns control to the host without waiting for a response from Notehub.
        file (str): The name of the local-only Database Notefile (`.dbx`) to be used if the web request is issued asynchronously and you wish to store the response.
        note (str): The unique Note ID for the local-only Database Notefile (`.dbx`). Only used with asynchronous web requests (see `file` argument above).

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "web.delete"}
    if route:
        req["route"] = route
    if name:
        req["name"] = name
    if content:
        req["content"] = content
    if seconds is not None:
        req["seconds"] = seconds
    if async_ is not None:
        req["async"] = async_
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    return card.Transaction(req)


@validate_card_object
def get(card, route=None, name=None, body=None, content=None, seconds=None, async_=None, binary=None, offset=None, max=None, file=None, note=None):
    """Perform a simple HTTP or HTTPS `GET` request against an external endpoint, and returns the response to the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        route (str): Alias for a Proxy Route in Notehub.
        name (str): A web URL endpoint relative to the host configured in the Proxy Route. URL parameters may be added to this argument as well (e.g. `/getLatest?id=1`).
        body (dict): The JSON body to send with the request.
        content (str): The MIME type of the body or payload of the response. Default is `application/json`.
        seconds (int): If specified, overrides the default 90 second timeout.
        async_ (bool): If `true`, the Notecard performs the web request asynchronously, and returns control to the host without waiting for a response from Notehub.
        binary (bool): If `true`, the Notecard will return the response stored in its binary buffer.
        offset (int): Used along with `binary:true` and `max`, sent as a URL parameter to the remote endpoint. Represents the number of bytes to offset the binary payload from 0 when retrieving binary data from the remote endpoint.
        max (int): Used along with `binary:true` and `offset`, sent as a URL parameter to the remote endpoint. Represents the number of bytes to retrieve from the binary payload segment.
        file (str): The name of the local-only Database Notefile (`.dbx`) to be used if the web request is issued asynchronously and you wish to store the response.
        note (str): The unique Note ID for the local-only Database Notefile (`.dbx`). Only used with asynchronous web requests (see `file` argument above).

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "web.get"}
    if route:
        req["route"] = route
    if name:
        req["name"] = name
    if body:
        req["body"] = body
    if content:
        req["content"] = content
    if seconds is not None:
        req["seconds"] = seconds
    if async_ is not None:
        req["async"] = async_
    if binary is not None:
        req["binary"] = binary
    if offset is not None:
        req["offset"] = offset
    if max is not None:
        req["max"] = max
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    return card.Transaction(req)


@validate_card_object
def post(card, route=None, name=None, body=None, payload=None, content=None, seconds=None, total=None, offset=None, status=None, max=None, verify=None, async_=None, binary=None, file=None, note=None):
    """Perform a simple HTTP or HTTPS `POST` request against an external endpoint, and returns the response to the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        route (str): Alias for a Proxy Route in Notehub.
        name (str): A web URL endpoint relative to the host configured in the Proxy Route. URL parameters may be added to this argument as well (e.g. `/addReading?id=1`).
        body (dict): The JSON body to send with the request.
        payload (str): A base64-encoded binary payload. A `web.post` may have either a `body` or a `payload`, but may NOT have both. Be aware that Notehub will decode the payload as it is delivered to the endpoint. Learn more about sending large binary objects with the Notecard.
        content (str): The MIME type of the body or payload of the response. Default is `application/json`.
        seconds (int): If specified, overrides the default 90 second timeout.
        total (int): When sending large payloads to Notehub in fragments across several `web.post` requests, the total size, in bytes, of the binary payload across all fragments.
        offset (int): When sending payload fragments, the number of bytes of the binary payload to offset from 0 when reassembling on the Notehub once all fragments have been received.
        status (str): A 32-character hex-encoded MD5 sum of the payload or payload fragment. Used by Notehub to perform verification upon receipt.
        max (int): The maximum size of the response from the remote server, in bytes. Useful if a memory-constrained host wants to limit the response size.
        verify (bool): `true` to request verification from Notehub once the payload or payload fragment is received. Automatically set to `true` when `status` is supplied.
        async_ (bool): If `true`, the Notecard performs the web request asynchronously, and returns control to the host without waiting for a response from Notehub.
        binary (bool): If `true`, the Notecard will send all the data in the binary buffer to the specified proxy route in Notehub. Learn more in this guide on Sending and Receiving Large Binary Objects.
        file (str): The name of the local-only Database Notefile (`.dbx`) to be used if the web request is issued asynchronously and you wish to store the response.
        note (str): The unique Note ID for the local-only Database Notefile (`.dbx`). Only used with asynchronous web requests (see `file` argument above).

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "web.post"}
    if route:
        req["route"] = route
    if name:
        req["name"] = name
    if body:
        req["body"] = body
    if payload:
        req["payload"] = payload
    if content:
        req["content"] = content
    if seconds is not None:
        req["seconds"] = seconds
    if total is not None:
        req["total"] = total
    if offset is not None:
        req["offset"] = offset
    if status:
        req["status"] = status
    if max is not None:
        req["max"] = max
    if verify is not None:
        req["verify"] = verify
    if async_ is not None:
        req["async"] = async_
    if binary is not None:
        req["binary"] = binary
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    return card.Transaction(req)


@validate_card_object
def put(card, route=None, name=None, body=None, payload=None, content=None, seconds=None, total=None, offset=None, status=None, max=None, verify=None, async_=None, file=None, note=None):
    """Perform a simple HTTP or HTTPS `PUT` request against an external endpoint, and returns the response to the Notecard.

    Args:
        card (Notecard): The current Notecard object.
        route (str): Alias for a Proxy Route in Notehub.
        name (str): A web URL endpoint relative to the host configured in the Proxy Route. URL parameters may be added to this argument as well (e.g. `/updateReading?id=1`).
        body (dict): The JSON body to send with the request.
        payload (str): A base64-encoded binary payload. A `web.put` may have either a `body` or a `payload`, but may NOT have both. Be aware that Notehub will decode the payload as it is delivered to the endpoint. Learn more about sending large binary objects with the Notecard.
        content (str): The MIME type of the body or payload of the response. Default is `application/json`.
        seconds (int): If specified, overrides the default 90 second timeout.
        total (int): When sending large payloads to Notehub in fragments across several `web.put` requests, the total size, in bytes, of the binary payload across all fragments.
        offset (int): When sending payload fragments, the number of bytes of the binary payload to offset from 0 when reassembling on the Notehub once all fragments have been received.
        status (str): A 32-character hex-encoded MD5 sum of the payload or payload fragment. Used by Notehub to perform verification upon receipt.
        max (int): The maximum size of the response from the remote server, in bytes. Useful if a memory-constrained host wants to limit the response size. Default (and maximum value) is 8192.
        verify (bool): `true` to request verification from Notehub once the payload or payload fragment is received. Automatically set to `true` when `status` is supplied.
        async_ (bool): If `true`, the Notecard performs the web request asynchronously, and returns control to the host without waiting for a response from Notehub.
        file (str): The name of the local-only Database Notefile (`.dbx`) to be used if the web request is issued asynchronously and you wish to store the response.
        note (str): The unique Note ID for the local-only Database Notefile (`.dbx`). Only used with asynchronous web requests (see `file` argument above).

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "web.put"}
    if route:
        req["route"] = route
    if name:
        req["name"] = name
    if body:
        req["body"] = body
    if payload:
        req["payload"] = payload
    if content:
        req["content"] = content
    if seconds is not None:
        req["seconds"] = seconds
    if total is not None:
        req["total"] = total
    if offset is not None:
        req["offset"] = offset
    if status:
        req["status"] = status
    if max is not None:
        req["max"] = max
    if verify is not None:
        req["verify"] = verify
    if async_ is not None:
        req["async"] = async_
    if file:
        req["file"] = file
    if note:
        req["note"] = note
    return card.Transaction(req)


@validate_card_object
def web(card, route=None, method=None, name=None, content=None):
    """Perform an HTTP or HTTPS request against an external endpoint, with the ability to specify any valid HTTP method.

    Args:
        card (Notecard): The current Notecard object.
        route (str): Alias for a Proxy Route in Notehub.
        method (str): The HTTP method of the request. Must be one of GET, PUT, POST, DELETE, PATCH, HEAD, OPTIONS, TRACE, or CONNECT.
        name (str): A web URL endpoint relative to the host configured in the Proxy Route. URL parameters may be added to this argument as well (e.g. `/getLatest?id=1`).
        content (str): The MIME type of the body or payload of the response. Default is `application/json`.

    Returns:
        dict: The result of the Notecard request.
    """
    req = {"req": "web"}
    if route:
        req["route"] = route
    if method:
        req["method"] = method
    if name:
        req["name"] = name
    if content:
        req["content"] = content
    return card.Transaction(req)
