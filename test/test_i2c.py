import os
import sys
import pytest
import re
from unittest.mock import MagicMock, patch
from .unit_test_utils import TrueOnNthIteration, BooleanToggle

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402


@pytest.fixture
def arrange_test():
    def _arrange_test(address=0, max_transfer=0, debug=False,
                      mock_locking=True):
        # OpenI2C's __init__ will call Reset, which we don't care about
        # actually doing here, so we mock Reset.
        with patch('notecard.notecard.OpenI2C.Reset'):
            card = notecard.OpenI2C(MagicMock(), address, max_transfer,
                                    debug)

        if mock_locking:
            card.lock = MagicMock()
            card.unlock = MagicMock()

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
        card._write = MagicMock()
        card._read = MagicMock()

        return card

    yield _arrange_reset_test


@pytest.fixture
def arrange_transact_test(arrange_test):
    def _arrange_transact_test():
        card = arrange_test()
        card.transmit = MagicMock()
        card.receive = MagicMock()
        req_bytes = card._prepare_request({'req': 'card.version'})

        return card, req_bytes

    yield _arrange_transact_test


@pytest.fixture
def arrange_read_test(arrange_test):
    def _arrange_read_test(available, data_len, data):
        def _platform_read_side_effect(initiate_read_msg, read_buf):
            read_buf[0] = available
            read_buf[1] = data_len
            read_buf[2:] = data

        card = arrange_test()
        card._platform_read = MagicMock(
            side_effect=_platform_read_side_effect)

        return card

    yield _arrange_read_test


class TestI2C:
    # Reset tests.
    def test_reset_succeeds_on_good_notecard_response(
            self, arrange_reset_test):
        card = arrange_reset_test()
        card._read.return_value = (0, b'\r\n')

        with patch('notecard.notecard.has_timed_out',
                   side_effect=TrueOnNthIteration(2)):
            card.Reset()

        assert not card._reset_required

    def test_reset_sends_a_newline_to_clear_stale_response(
            self, arrange_reset_test):
        card = arrange_reset_test()
        card._read.return_value = (0, b'\r\n')

        with patch('notecard.notecard.has_timed_out',
                   side_effect=TrueOnNthIteration(2)):
            card.Reset()

        card._write.assert_called_once_with(b'\n')

    def test_reset_locks_and_unlocks(self, arrange_reset_test):
        card = arrange_reset_test()
        card._read.return_value = (0, b'\r\n')

        with patch('notecard.notecard.has_timed_out',
                   side_effect=TrueOnNthIteration(2)):
            card.Reset()

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_reset_unlocks_after_exception(self, arrange_reset_test):
        card = arrange_reset_test()
        card._write.side_effect = Exception('write failed.')

        with pytest.raises(Exception, match='Failed to reset Notecard.'):
            card.Reset()

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_reset_fails_if_continually_reads_non_control_chars(
            self, arrange_reset_test):
        card = arrange_reset_test()
        card._read.return_value = (1, 1, b'h')

        with patch('notecard.notecard.has_timed_out',
                   side_effect=BooleanToggle(False)):
            with pytest.raises(Exception, match='Failed to reset Notecard.'):
                card.Reset()

    def test_reset_required_if_reset_fails(self, arrange_reset_test):
        card = arrange_reset_test()
        card._write.side_effect = Exception('write failed.')

        with pytest.raises(Exception, match='Failed to reset Notecard.'):
            card.Reset()

        assert card._reset_required

    # __init__ tests.
    def test_init_calls_reset(self):
        with patch('notecard.notecard.OpenI2C.Reset') as reset_mock:
            notecard.OpenI2C(MagicMock(), 0, 0)

            reset_mock.assert_called_once()

    @pytest.mark.parametrize(
        'addr_param,expected_addr',
        [
            (0, notecard.NOTECARD_I2C_ADDRESS),
            (7, 7)
        ]
    )
    def test_init_sets_address_correctly(
            self, addr_param, expected_addr, arrange_test):
        card = arrange_test(address=addr_param)

        assert card.addr == expected_addr

    @pytest.mark.parametrize(
        'max_param,expected_max',
        [
            (0, notecard.NOTECARD_I2C_MAX_TRANSFER_DEFAULT),
            (7, 7)
        ]
    )
    def test_init_sets_max_transfer_correctly(
            self, max_param, expected_max, arrange_test):
        card = arrange_test(max_transfer=max_param)

        assert card.max == expected_max

    @pytest.mark.parametrize('debug_param', [False, True])
    def test_init_sets_debug_correctly(self, debug_param, arrange_test):
        card = arrange_test(debug=debug_param)

        assert card._debug == debug_param

    @pytest.mark.parametrize('use_i2c_lock', [False, True])
    def test_init_uses_appropriate_locking_functions(
            self, use_i2c_lock, arrange_test):
        with patch('notecard.notecard.use_i2c_lock', new=use_i2c_lock):
            card = arrange_test()

            if use_i2c_lock:
                assert card.lock_fn == card.i2c.try_lock
                assert card.unlock_fn == card.i2c.unlock
            else:
                assert card.lock_fn.__func__ == \
                       notecard.OpenI2C._i2c_no_op_try_lock
                assert card.unlock_fn.__func__ == \
                       notecard.OpenI2C._i2c_no_op_unlock

    @pytest.mark.parametrize(
        'platform,write_method,read_method',
        [
            (
                'micropython',
                notecard.OpenI2C._non_cpython_write,
                notecard.OpenI2C._micropython_read
            ),
            (
                'circuitpython',
                notecard.OpenI2C._non_cpython_write,
                notecard.OpenI2C._circuitpython_read
            ),
            (
                'cpython',
                notecard.OpenI2C._cpython_write,
                notecard.OpenI2C._cpython_read
            ),
        ]
    )
    def test_init_sets_platform_hooks_correctly(
            self, platform, write_method, read_method, arrange_test):
        with patch('notecard.notecard.sys.implementation.name', new=platform):
            card = arrange_test()

        assert card._platform_write.__func__ == write_method
        assert card._platform_read.__func__ == read_method

    def test_user_agent_indicates_i2c_after_init(self, arrange_test):
        card = arrange_test()
        userAgent = card.GetUserAgent()

        assert userAgent['req_interface'] == 'i2c'
        assert userAgent['req_port'] is not None

    # receive tests.
    def test_receive_returns_all_data_bytes_from_read(self, arrange_test):
        card = arrange_test()
        payload = b'{}\r\n'
        card._read = MagicMock()
        card._read.side_effect = [
            # There are 4 bytes available to read, and there are no more bytes
            # to read in this packet.
            (4, bytearray()),
            # 0 bytes available to read after this packet. 4 coming in this
            # packet, and they are {}\r\n.
            (0, payload)
        ]

        rx_data = card.receive()

        assert rx_data == payload

    def test_receive_keeps_reading_if_data_available_after_newline(
            self, arrange_test):
        card = arrange_test()
        payload = b'{}\r\n'
        excess_data = b'io'
        card._read = MagicMock()
        card._read.side_effect = [
            # There are 4 bytes available to read, and there are no more bytes
            # to read in this packet.
            (4, bytearray()),
            # 2 bytes available to read after this packet. 4 coming in this
            # packet, and they are {}\r\n.
            (2, payload),
            # 0 bytes after this packet. 2 coming in this packet, and they are
            # io.
            (0, excess_data)
        ]

        rx_data = card.receive()

        assert rx_data == (payload + excess_data)

    def test_receive_raises_exception_on_timeout(self, arrange_test):
        card = arrange_test()
        payload = b'{}\r'
        card._read = MagicMock()
        card._read.side_effect = [
            # There are 3 bytes available to read, and there are no more bytes
            # to read in this packet.
            (3, bytearray()),
            # 0 bytes available to read after this packet. 3 coming in this
            # packet, and they are {}\r. The lack of a newline at the end will
            # cause this test to hit the timeout.
            (0, payload)
        ]

        with patch('notecard.notecard.has_timed_out', return_value=True):
            with pytest.raises(Exception, match=('Timed out while reading '
                                                 'data from the Notecard.')):
                card.receive()

    # transmit tests.
    def test_transmit_writes_all_data_bytes(self, arrange_test):
        card = arrange_test()
        # Create a bytearray to transmit. It should be larger than a single I2C
        # chunk (i.e. greater than card.max), and it should not fall neatly onto
        # a segment boundary.
        data_len = card.max * 2 + 15
        data = bytearray(i % 256 for i in range(data_len))
        write_mock = MagicMock()
        card._write = write_mock

        card.transmit(data)

        # Using the argument history of the _write mock, assemble a bytearray of
        # the data passed to write.
        written = bytearray()
        for write_call in write_mock.call_args_list:
            segment = write_call[0][0]
            written += segment

        # Verify that all the data we passed to transmit was in fact passed to
        # uart.write.
        assert data == written

    def test_transmit_does_not_exceed_max_transfer_size(self, arrange_test):
        card = arrange_test()
        # Create a bytearray to transmit. It should be larger than a single
        # I2C chunk (i.e. greater than card.max), and it should not fall neatly
        # onto a segment boundary.
        data_len = card.max * 2 + 15
        data = bytearray(i % 256 for i in range(data_len))
        write_mock = MagicMock()
        card._write = write_mock

        card.transmit(data)

        for write_call in write_mock.call_args_list:
            assert len(write_call[0][0]) <= card.max

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
        card._read = MagicMock(return_value=(1, bytearray()))

        rsp = card._transact(req_bytes, rsp_expected=True)

        assert rsp is not None

    def test_transact_calls_receive_if_rsp_expected(
            self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()
        card._read = MagicMock(return_value=(1, bytearray()))

        card._transact(req_bytes, rsp_expected=True)

        card.receive.assert_called_once()

    def test_transact_raises_exception_on_timeout(self, arrange_transact_test):
        card, req_bytes = arrange_transact_test()
        card._read = MagicMock(return_value=(0, bytearray()))

        # Force a timeout.
        with patch('notecard.notecard.has_timed_out',
                   side_effect=BooleanToggle(False)):
            with pytest.raises(Exception,
                               match=('Timed out while querying Notecard for '
                                      'available data.')):
                card._transact(req_bytes, rsp_expected=True)

    # _read tests.
    def test_read_sends_the_initial_read_packet_correctly(
            self, arrange_read_test):
        data_len = 4
        data = b'\xDE\xAD\xBE\xEF'
        card = arrange_read_test(0, data_len, data)
        # To start a read from the Notecard using serial-over-I2C, the host
        # should send a 0 byte followed by a byte with the requested read
        # length.
        expected_packet = bytearray(2)
        expected_packet[0] = 0
        expected_packet[1] = data_len

        card._read(data_len)

        card._platform_read.assert_called_once()
        assert card._platform_read.call_args[0][0] == expected_packet

    def test_read_sizes_read_buf_correctly(self, arrange_read_test):
        data_len = 4
        data = b'\xDE\xAD\xBE\xEF'
        card = arrange_read_test(0, data_len, data)
        header_len = 2
        expected_read_buffer_len = header_len + data_len

        card._read(data_len)

        card._platform_read.assert_called_once()
        assert len(card._platform_read.call_args[0][1]) == \
               expected_read_buffer_len

    def test_read_parses_data_correctly(self, arrange_read_test):
        available = 8
        data_len = 4
        data = b'\xDE\xAD\xBE\xEF'
        card = arrange_read_test(available, data_len, data)

        actual_available, actual_data = card._read(len(data))

        card._platform_read.assert_called_once()
        assert actual_available == available
        assert actual_data == data

    def test_read_raises_exception_if_data_length_does_not_match_data(
            self, arrange_read_test):
        available = 8
        # The reported length is 5, but the actual length is 4.
        data_len = 5
        data = b'\xDE\xAD\xBE\xEF'
        card = arrange_read_test(available, data_len, data)

        exception_msg = re.escape(('Serial-over-I2C error: reported data length'
                                   f' ({data_len}) differs from actual data '
                                   f'length ({len(data)}).'))
        with pytest.raises(Exception, match=exception_msg):
            card._read(len(data))

    # _write tests.
    def test_write_calls_platform_write_correctly(self, arrange_test):
        card = arrange_test()
        card._platform_write = MagicMock()
        data = bytearray([0xDE, 0xAD, 0xBE, 0xEF])

        card._write(data)

        card._platform_write.assert_called_once_with(
            bytearray([len(data)]), data)

    # lock tests.
    def test_lock_calls_lock_fn(self, arrange_test):
        card = arrange_test(mock_locking=False)
        card.lock_fn = MagicMock(return_value=True)

        card.lock()

        card.lock_fn.assert_called()

    def test_lock_retries_lock_fn_if_needed(self, arrange_test):
        card = arrange_test(mock_locking=False)
        # Fails the first time and succeeds the second time.
        card.lock_fn = MagicMock(side_effect=[False, True])

        card.lock()

        assert card.lock_fn.call_count == 2

    def test_lock_raises_exception_if_lock_fn_never_returns_true(
            self, arrange_test):
        card = arrange_test(mock_locking=False)
        card.lock_fn = MagicMock(return_value=False)

        with pytest.raises(Exception, match='Failed to acquire I2C lock.'):
            card.lock()

    # unlock tests.
    def test_unlock_calls_unlock_fn(self, arrange_test):
        card = arrange_test(mock_locking=False)
        card.unlock_fn = MagicMock()

        card.unlock()

        card.unlock_fn.assert_called()
