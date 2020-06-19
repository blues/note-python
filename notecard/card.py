import notecard


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
