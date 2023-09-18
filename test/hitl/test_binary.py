import pyboard
import pytest
from example_runner import ExampleRunner


@pytest.mark.parametrize('use_uart', [False, True])
def test_binary(pytestconfig, use_uart):
    runner = ExampleRunner(pytestconfig.port, 'binary_loopback_example.py',
                           pytestconfig.product_uid)
    runner.run(use_uart)
