import notecard


def changes(card, file=None, tracker=None, max=None,
            start=None, stop=None, deleted=None, delete=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "note.changes"}
    if file:
        req["file"] = file
    if tracker:
        req["tracker"] = tracker
    if max:
        req["max"] = max
    if start:
        req["start"] = start
    if stop:
        req["stop"] = stop
    if deleted:
        req["deleted"] = deleted
    if delete:
        req["delete"] = delete
    return card.Transaction(req)


def get(card, file="data.qi", note_id=None, delete=None, deleted=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "note.get"}
    req["file"] = file
    if note_id:
        req["note"] = note_id
    if delete:
        req["delete"] = delete
    if deleted:
        req["deleted"] = deleted
    return card.Transaction(req)


def delete(card, file=None, note_id=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "note.delete"}
    if file:
        req["file"] = file
    if note_id:
        req["note"] = note_id
    return card.Transaction(req)


def update(card, file=None, note_id=None, body=None, payload=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "note.get"}
    if file:
        req["file"] = file
    if note_id:
        req["note"] = note_id
    if body:
        req["body"] = body
    if payload:
        req["payload"] = payload
    return card.Transaction(req)
