import notecard


def get(card, name=None):
    if not isinstance(card, notecard.Notecard):
        raise Exception("Notecard object required")

    req = {"req": "env.get"}
    if name:
        req["name"] = name
    return card.Transaction(req)
