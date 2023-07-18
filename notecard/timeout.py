"""Module for managing timeouts in note-python."""

import sys
import time

use_rtc = sys.implementation.name != 'micropython' and sys.implementation.name != 'circuitpython'

if not use_rtc:
    if sys.implementation.name == 'circuitpython':
        import supervisor
        from supervisor import ticks_ms

        _TICKS_PERIOD = 1 << 29
        _TICKS_MAX = _TICKS_PERIOD - 1
        _TICKS_HALFPERIOD = _TICKS_PERIOD // 2

        def ticks_diff(ticks1, ticks2):
            """Compute the signed difference between two ticks values."""
            diff = (ticks1 - ticks2) & _TICKS_MAX  # noqa: F821
            diff = ((diff + _TICKS_HALFPERIOD)  # noqa: F821
                    & _TICKS_MAX) - _TICKS_HALFPERIOD  # noqa: F821
            return diff

    if sys.implementation.name == 'micropython':
        from utime import ticks_diff, ticks_ms  # noqa: F811


def has_timed_out(start, timeout_secs):
    """Determine whether a timeout interval has passed during communication."""
    if not use_rtc:
        return ticks_diff(ticks_ms(), start) > timeout_secs * 1000
    else:
        return time.time() > start + timeout_secs


def start_timeout():
    """Start the timeout interval for I2C communication."""
    return ticks_ms() if not use_rtc else time.time()
