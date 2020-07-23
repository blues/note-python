import notecard


def changes(card, tracker=None, files=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "file.changes"}
    if tracker:
        req["tracker"] = tracker
    if files:
        req["files"] = files
    return card.Transaction(req)


def delete(card, files=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "file.delete"}
    if files:
        req["files"] = files
    return card.Transaction(req)


def stats(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "file.stats"}

    return card.Transaction(req)


def pendingChanges(card):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "file.changes.pending"}

    return card.Transaction(req)
