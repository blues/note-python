import os
import sys
import pytest
from unittest.mock import MagicMock, patch
from filelock import FileLock
from contextlib import AbstractContextManager
from .unit_test_utils import TrueOnNthIteration, BooleanToggle

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402
from notecard import NoOpSerialLock, NoOpContextManager  # noqa: E402


@pytest.fixture
def arrange_test():
    def _arrange_test(debug=False):
        # OpenSerial's __init__ will call Reset, which we don't care about
        # actually doing here, so we mock Reset.
        with patch('notecard.notecard.OpenSerial.Reset'):
            card = notecard.OpenSerial(MagicMock(), debug=debug)

        return card

    # Mocking time.sleep makes the tests run faster because no actual sleeping
    # occurs.
    with patch('notecard.notecard.time.sleep'):
        # Yield instead of return so that the time.sleep patch is active for the
        # duration of the test.
        yield _arrange_test


@pytest.fixture
def arrange_reset_test(arrange_test):
    def _arrange_reset_test():
        card = arrange_test()
        card.lock = MagicMock()
        card.unlock = MagicMock()
        card.uart.write = MagicMock()

        return card

    yield _arrange_reset_test


@pytest.fixture
def tramsit_test_data():
    # Create a bytearray to transmit. It should be larger than a single segment,
    # and it should not fall neatly onto a segment boundary.
    data_len = notecard.CARD_REQUEST_SEGMENT_MAX_LEN * 2 + 15
    data = bytearray(i % 256 for i in range(data_len))

    return data


@pytest.fixture
def arrange_transact_test(arrange_test):
    def _arrange_transact_test():
        card = arrange_test()
        card.transmit = MagicMock()
        card.receive = MagicMock()
        req_bytes = card._prepare_request({'req': 'card.version'})

        return card, req_bytes

    yield _arrange_transact_test


class TestSerial:
    # Reset tests.
    def test_reset_succeeds_on_good_notecard_response(self, arrange_reset_test):
        card = arrange_reset_test()
        card._available = MagicMock(side_effect=[True, True, False])
        card._read_byte = MagicMock(side_effect=[b'\r', b'\n', None])

        with patch('notecard.notecard.has_timed_out',
                   side_effect=TrueOnNthIteration(2)):
            card.Reset()

        assert not card._reset_required

    def test_reset_sends_a_newline_to_clear_stale_response(
            self, arrange_reset_test):
        card = arrange_reset_test()
        card._available = MagicMock(side_effect=[True, True, False])
        card._read_byte = MagicMock(side_effect=[b'\r', b'\n', None])

        with patch('notecard.notecard.has_timed_out',
                   side_effect=TrueOnNthIteration(2)):
            card.Reset()

        card.uart.write.assert_called_once_with(b'\n')

    def test_reset_locks_and_unlocks(self, arrange_reset_test):
        card = arrange_reset_test()
        card._available = MagicMock(side_effect=[True, True, False])
        card._read_byte = MagicMock(side_effect=[b'\r', b'\n', None])

        with patch('notecard.notecard.has_timed_out',
                   side_effect=TrueOnNthIteration(2)):
            card.Reset()

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_reset_unlocks_after_exception(self, arrange_reset_test):
        card = arrange_reset_test()
        card.uart.write.side_effect = Exception('write failed.')

        with pytest.raises(Exception, match='Failed to reset Notecard.'):
            card.Reset()

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_reset_fails_if_continually_reads_non_control_chars(
            self, arrange_reset_test):
        card = arrange_reset_test()
        card._available = MagicMock(side_effect=BooleanToggle(True))
        card._read_byte = MagicMock(return_value=b'h')

        with patch('notecard.notecard.has_timed_out',
                   side_effect=BooleanToggle(False)):
            with pytest.raises(Exception, match='Failed to reset Notecard.'):
                card.Reset()

    def test_reset_required_if_reset_fails(self, arrange_reset_test):
        card = arrange_reset_test()
        card.uart.write.side_effect = Exception('write failed.')

        with pytest.raises(Exception, match='Failed to reset Notecard.'):
            card.Reset()

        assert card._reset_required

    # __init__ tests.
    @patch('notecard.notecard.OpenSerial.Reset')
    def test_init_calls_reset(self, reset_mock):
        notecard.OpenSerial(MagicMock())

        reset_mock.assert_called_once()

    @pytest.mark.parametrize(
        'use_serial_lock,lock_type',
        [
            (False, NoOpSerialLock),
            (True, FileLock)
        ]
    )
    def test_init_creates_appropriate_lock_type(
            self, use_serial_lock, lock_type, arrange_test):
        with patch('notecard.notecard.use_serial_lock', new=use_serial_lock):
            card = arrange_test()

        assert isinstance(card.lock_handle, lock_type)

    def test_init_fails_if_not_micropython_and_uart_has_no_in_waiting_attr(
            self):
        exception_msg = ('Serial communications with the Notecard are not '
                         'supported for this platform.')

        with patch('notecard.notecard.sys.implementation.name', new='cpython'):
            with patch('notecard.notecard.OpenSerial.Reset'):
                with pytest.raises(Exception, match=exception_msg):
                    notecard.OpenSerial(42)

    @pytest.mark.parametrize(
        'platform,available_method',
        [
            ('micropython', notecard.OpenSerial._available_micropython),
            ('cpython', notecard.OpenSerial._available_default),
            ('circuitpython', notecard.OpenSerial._available_default),
        ]
    )
    def test_available_method_is_set_correctly_on_init(
            self, platform, available_method, arrange_test):
        with patch('notecard.notecard.sys.implementation.name', new=platform):
            card = arrange_test()

        assert card._available.__func__ == available_method

    @pytest.mark.parametrize('debug', [False, True])
    def test_debug_set_correctly_on_init(self, debug, arrange_test):
        card = arrange_test(debug)

        assert card._debug == debug

    def test_user_agent_indicates_serial_after_init(self, arrange_test):
        card = arrange_test()
        userAgent = card.GetUserAgent()

        assert userAgent['req_interface'] == 'serial'
        assert userAgent['req_port'] is not None

    # _transact tests.
    def test_transact_calls_transmit_with_req_bytes(
            self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()

        card._transact(req_bytes, rsp_expected=False)

        card.transmit.assert_called_once_with(req_bytes)

    def test_transact_returns_none_if_rsp_not_expected(
            self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()

        rsp = card._transact(req_bytes, rsp_expected=False)

        assert rsp is None

    def test_transact_returns_not_none_if_rsp_expected(
            self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()
        card._available = MagicMock(return_value=True)

        rsp = card._transact(req_bytes, rsp_expected=True)

        assert rsp is not None

    def test_transact_calls_receive_if_rsp_expected(
            self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()
        card._available = MagicMock(return_value=True)

        card._transact(req_bytes, rsp_expected=True)

        card.receive.assert_called_once()

    def test_transact_raises_exception_on_timeout(self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()
        card._available = MagicMock(return_value=False)

        # Force a timeout.
        with patch('notecard.notecard.has_timed_out',
                   side_effect=BooleanToggle(False)):
            with pytest.raises(Exception,
                               match=('Timed out while querying Notecard for '
                                      'available data.')):
                card._transact(req_bytes, rsp_expected=True)

    # transmit tests.
    def test_transmit_writes_all_data_bytes(
            self, arrange_test, tramsit_test_data):
        card = arrange_test()
        card.uart.write = MagicMock()

        card.transmit(tramsit_test_data, True)

        # Using the argument history of the uart.write mock, assemble a
        # bytearray of the data passed to uart.write.
        written = bytearray()
        for write_call in card.uart.write.call_args_list:
            segment = write_call[0][0]
            written += segment
        # Verify that all the data we passed to transmit was in fact passed to
        # uart.write.
        assert tramsit_test_data == written

    def test_transmit_does_not_exceed_max_segment_length(
            self, arrange_test, tramsit_test_data):
        card = arrange_test()
        card.uart.write = MagicMock()

        card.transmit(tramsit_test_data)

        for write_call in card.uart.write.call_args_list:
            segment = write_call.args[0]
            assert len(segment) <= notecard.CARD_REQUEST_SEGMENT_MAX_LEN

    # receive tests.
    def test_receive_raises_exception_on_timeout(self, arrange_test):
        card = arrange_test()
        card._available = MagicMock(return_value=False)

        # Force a timeout.
        with patch('notecard.notecard.has_timed_out',
                   side_effect=[False, True]):
            with pytest.raises(Exception, match=('Timed out waiting to receive '
                                                 'data from Notecard.')):
                card.receive()

    def test_receive_returns_all_bytes_from_read_byte(
            self, arrange_test):
        card = arrange_test()
        read_byte_mock = MagicMock()
        read_byte_mock.side_effect = [b'{', b'}', b'\r', b'\n']
        card._read_byte = read_byte_mock
        card._available = MagicMock(return_value=True)
        expected_data = bytearray('{}\r\n'.encode('utf-8'))

        data = card.receive()

        # Verify that all the bytes returned by _read_byte were returned as a
        # bytearray by receive.
        assert data == expected_data

    # _read_byte tests.
    def test_read_byte_calls_uart_read(self, arrange_test):
        card = arrange_test()
        card.uart.read = MagicMock()

        card._read_byte()

        card.uart.read.assert_called_once_with(1)

    # NoOpSerialLock tests.
    def test_no_op_serial_lock_implements_acquire_and_release(self):
        no_op_lock = NoOpSerialLock()

        assert hasattr(no_op_lock, 'acquire')
        assert hasattr(no_op_lock, 'release')

    def test_no_op_serial_lock_acquire_returns_no_op_context_manager(self):
        no_op_lock = NoOpSerialLock()

        assert isinstance(no_op_lock.acquire(), NoOpContextManager)

    def test_no_op_serial_lock_acquire_accepts_timeout_arg(self):
        no_op_lock = NoOpSerialLock()

        no_op_lock.acquire(timeout=10)

    # NoOpContextManager tests.
    def test_no_op_context_manager_is_a_context_manager(self):
        manager = NoOpContextManager()

        with manager:
            pass

        assert isinstance(manager, AbstractContextManager)

    # lock/unlock tests.
    def test_lock_calls_acquire_on_underlying_lock(self, arrange_test):
        card = arrange_test()
        lock_handle_mock = MagicMock()
        card.lock_handle = lock_handle_mock

        card.lock()

        lock_handle_mock.acquire.assert_called_once()

    def test_unlock_calls_release_on_underlying_lock(self, arrange_test):
        card = arrange_test()
        lock_handle_mock = MagicMock()
        card.lock_handle = lock_handle_mock

        card.unlock()

        lock_handle_mock.release.assert_called_once()
