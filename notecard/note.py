import notecard


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
