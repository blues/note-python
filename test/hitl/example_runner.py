import pyboard


class ExampleRunner:
    def __init__(self, pyboard_port, example_file, product_uid):
        self.pyboard_port = pyboard_port
        self.example_module = example_file[:-3]  # Remove .py suffix.
        self.product_uid = product_uid

    def run(self, use_uart, assert_success=True):
        pyb = pyboard.Pyboard(self.pyboard_port, 115200)
        pyb.enter_raw_repl()
        try:
            cmd = f'from {self.example_module} import run_example; run_example("{self.product_uid}", {use_uart})'
            output = pyb.exec(cmd)
            output = output.decode()
        finally:
            pyb.exit_raw_repl()
            pyb.close()

        print(output)
        assert 'Example complete.' in output
        return output
