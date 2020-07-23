import notecard


def attn(card, mode=None, files=None, seconds=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "card.attn"}
    if mode:
        req["mode"] = mode
    if files:
        req["files"] = files
    if seconds:
        req["seconds"] = seconds
    return card.Transaction(req)


def time(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "card.time"}
    return card.Transaction(req)


def status(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "card.status"}
    return card.Transaction(req)


def temp(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "card.temp"}
    return card.Transaction(req)


def version(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "card.version"}
    return card.Transaction(req)


def voltage(card, hours=None, offset=None, vmax=None, vmin=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

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


def wireless(card, mode=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "card.wireless"}
    if mode:
        req["mode"] = mode

    return card.Transaction(req)
