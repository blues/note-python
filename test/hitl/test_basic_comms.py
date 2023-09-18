import pyboard
import pytest
from example_runner import ExampleRunner


def run_basic_comms_test(config, use_uart):
    if config.platform == 'micropython':
        example_file = 'mpy_example.py'
    elif config.platform == 'circuitpython':
        example_file = 'cpy_example.py'
    else:
        raise Exception(f'Unsupported platform: {config.platform}')

    runner = ExampleRunner(config.port, example_file, config.product_uid)
    runner.run(use_uart)


@pytest.mark.parametrize('use_uart', [False, True])
def test_basic_comms(pytestconfig, use_uart):
    run_basic_comms_test(pytestconfig, use_uart)
