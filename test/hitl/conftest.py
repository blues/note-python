from pathlib import Path
import shutil
import sys

# Add the 'deps' folder to the path so we can import the pyboard module from
# it.
deps_path = str(Path(__file__).parent / 'deps')
sys.path.append(deps_path)
import pyboard  # noqa: E402


def mkdir_on_host(pyb, dir):
    pyb.enter_raw_repl()
    try:
        pyb.fs_mkdir(dir)
    except pyboard.PyboardError as e:
        already_exists = ["EEXIST", "File exists"]
        if any([keyword in str(e) for keyword in already_exists]):
            # If the directory already exists, that's fine.
            pass
        else:
            raise
    finally:
        pyb.exit_raw_repl()


def copy_files_to_host(pyb, files, dest_dir):
    pyb.enter_raw_repl()
    try:
        for f in files:
            pyb.fs_put(f, f'{dest_dir}/{f.name}', chunk_size=4096)
    finally:
        pyb.exit_raw_repl()


def copy_file_to_host(pyb, file, dest):
    pyb.enter_raw_repl()
    try:
        pyb.fs_put(file, dest, chunk_size=4096)
    finally:
        pyb.exit_raw_repl()


def setup_host(port, platform, mpy_board):
    pyb = pyboard.Pyboard(port, 115200)
    # Get the path to the root of the note-python repository.
    note_python_root_dir = Path(__file__).parent.parent.parent
    notecard_dir = note_python_root_dir / 'notecard'
    # Get a list of all the .py files in note-python/notecard/.
    notecard_files = list(notecard_dir.glob('*.py'))

    mkdir_on_host(pyb, '/lib')
    mkdir_on_host(pyb, '/lib/notecard')
    copy_files_to_host(pyb, notecard_files, '/lib/notecard')

    # Copy over mpy_example.py. We'll run this example code on the MicroPython
    # host to 1) verify that the host is able to use note-python to communicate
    # with the Notecard and 2) verify that the example isn't broken.
    if platform == 'circuitpython':
        example_file = 'cpy_example.py'
    else:
        example_file = 'mpy_example.py'
        if mpy_board:
            boards_dir = note_python_root_dir / 'mpy_board'
            board_file_path = boards_dir / f"{mpy_board}.py"
            copy_file_to_host(pyb, board_file_path, '/board.py')

    examples_dir = note_python_root_dir / 'examples'
    example_file_path = examples_dir / 'notecard-basics' / example_file
    copy_file_to_host(pyb, example_file_path, '/example.py')

    pyb.close()


def pytest_addoption(parser):
    parser.addoption(
        '--port',
        required=True,
        help='The serial port of the MCU host (e.g. /dev/ttyACM0).'
    )
    parser.addoption(
        '--platform',
        required=True,
        help='Choose the platform to run the tests on.',
        choices=["circuitpython", "micropython"]
    )
    parser.addoption(
        '--productuid',
        required=True,
        help='The ProductUID to set on the Notecard.'
    )
    parser.addoption(
        "--skipsetup",
        action="store_true",
        help="Skip host setup (copying over note-python, etc.) (default: False)"
    )
    parser.addoption(
        '--mpyboard',
        required=False,
        help='The board name that is being used. Required only when running micropython.'
    )


def pytest_configure(config):
    config.port = config.getoption("port")
    config.platform = config.getoption("platform")
    config.product_uid = config.getoption("productuid")
    config.skip_setup = config.getoption("skipsetup")
    config.mpy_board = config.getoption("mpyboard")

    if not config.skip_setup:
        setup_host(config.port, config.platform, config.mpy_board)
