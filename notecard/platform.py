"""Module for detecting the platform note-python is running on."""

import sys

platform = None

if sys.implementation.name == 'circuitpython':
    import digitalio
    platform = 'circuitpython'
elif sys.implementation.name == 'micropython':
    import machine
    platform = 'micropython'
elif sys.implementation.name == 'cpython':
    try:
        with open('/etc/os-release', 'r') as f:
            use_raspbian = 'ID=raspbian' in f.read()
    except IOError:
        pass

    if use_raspbian:
        platform = 'raspbian'
