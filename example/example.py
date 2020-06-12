import os
import sys

sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402

print(dir(notecard))

comms_card = notecard.OpenSerial()
