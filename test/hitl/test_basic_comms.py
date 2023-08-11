import pyboard
import pytest


def run_example(port, product_uid, use_uart):
    pyb = pyboard.Pyboard(port, 115200)
    pyb.enter_raw_repl()
    try:
        cmd = f'from example import run_example; run_example("{product_uid}", {use_uart})'
        output = pyb.exec(cmd)
        output = output.decode()
        print(output)
        assert 'Example complete.' in output
    finally:
        pyb.exit_raw_repl()
        pyb.close()

def test_example_i2c(pytestconfig):
    run_example(pytestconfig.port, pytestconfig.product_uid, use_uart=False)


def test_example_serial(pytestconfig):
    run_example(pytestconfig.port, pytestconfig.product_uid, use_uart=True)
