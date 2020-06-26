import notecard


def set(card, product, sn=None,
        mode=None, minutes=None, hours=None, sync=False):

    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "hub.set"}
    if product:
        req["product"] = product
    if sn:
        req["sn"] = sn
    if mode:
        req["mode"] = mode
    if minutes:
        req["minutes"] = minutes
    if hours:
        req["hours"] = hours
    if sync:
        req["sync"] = True

    return card.Transaction(req)


def sync(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "hub.sync"}
    return card.Transaction(req)


def syncStatus(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "hub.sync.status"}
    return card.Transaction(req)


def status(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "hub.status"}
    return card.Transaction(req)


def log(card, text, sync=False):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "hub.log"}
    req["text"] = text
    req["sync"] = sync
    return card.Transaction(req)


def get(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "hub.get"}
    return card.Transaction(req)
