"""TransactionManager-related code for note-python."""

import sys
import time

from notecard.timeout import start_timeout, has_timed_out
from notecard.gpio import GPIO


class TransactionManager:
    """Class for managing the start and end of Notecard transactions.

    Some Notecards need to be signaled via GPIO when a transaction is about to
    start. When the Notecard sees a particular GPIO, called RTX (ready to
    transact), go high, it responds with a high pulse on another GPIO, CTX
    (clear to transact). At this point, the transaction can proceed. This class
    implements this protocol in its start method.
    """

    def __init__(self, rtx_pin, ctx_pin):
        """Initialize the TransactionManager.

        Even though RTX is an output, we set it as an input here to conserve
        power until we need to use it.
        """
        self.rtx_pin = GPIO.setup(rtx_pin, GPIO.IN)
        self.ctx_pin = GPIO.setup(ctx_pin, GPIO.IN)

    def start(self, timeout_secs):
        """Prepare the Notecard for a transaction."""
        start = start_timeout()

        self.rtx_pin.direction(GPIO.OUT)
        self.rtx_pin.value(1)
        # If the Notecard supports RTX/CTX, it'll pull CTX low. If the Notecard
        # doesn't support RTX/CTX, this pull up will make sure we get the clear
        # to transact immediately.
        self.ctx_pin.pull(GPIO.PULL_UP)

        # Wait for the Notecard to signal clear to transact (i.e. drive the CTX
        # pin HIGH). Time out after timeout_secs seconds.
        while True:
            if self.ctx_pin.value():
                break

            if (has_timed_out(start, timeout_secs)):
                # Abandon request on timeout.
                self.stop()
                raise Exception(
                    "Timed out waiting for Notecard to give clear to transact."
                )

            time.sleep(.001)

        self.ctx_pin.pull(GPIO.PULL_NONE)

    def stop(self):
        """Make RTX an input to conserve power and remove the pull up on CTX."""
        self.rtx_pin.direction(GPIO.IN)
        self.ctx_pin.pull(GPIO.PULL_NONE)


class NoOpTransactionManager:
    """Class for transaction start/stop when no transaction pins are set.

    If the transaction pins aren't set, the start and stop operations should be
    no-ops.
    """

    def start(self, timeout_secs):
        """No-op start function."""
        pass

    def stop(self):
        """No-op stop function."""
        pass
