import os
import sys
import pytest
from unittest.mock import MagicMock, patch
import json
import re

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402
from notecard.transaction_manager import TransactionManager, NoOpTransactionManager  # noqa: E402


@pytest.fixture
def arrange_transaction_test():
    # Mocking time.sleep makes the tests run faster because no actual sleeping
    # occurs.
    with patch('notecard.notecard.time.sleep'):
        def _arrange_transaction_test():
            card = notecard.Notecard()
            card.Reset = MagicMock()
            card.lock = MagicMock()
            card.unlock = MagicMock()
            card._transact = MagicMock(return_value=b'{}\r\n')
            card._crc_error = MagicMock(return_value=False)

            return card

        # Yield instead of return so that the time.sleep patch is active for the
        # duration of the test.
        yield _arrange_transaction_test


class TestNotecard:
    # _transaction_manager tests.
    def test_txn_manager_is_no_op_before_pins_set(self):
        card = notecard.Notecard()

        assert isinstance(card._transaction_manager, NoOpTransactionManager)

    def test_txn_manager_is_valid_after_pins_set(self):
        card = notecard.Notecard()
        with patch('notecard.notecard.TransactionManager', autospec=True):
            card.SetTransactionPins(1, 2)

        assert isinstance(card._transaction_manager, TransactionManager)

    # _crc_add tests
    def test_crc_add_adds_a_crc_field(self):
        card = notecard.Notecard()
        req = '{"req":"hub.status"}'

        req_string = card._crc_add(req, 0)

        req_json = json.loads(req_string)
        assert 'crc' in req_json

    def test_crc_add_formats_the_crc_field_correctly(self):
        card = notecard.Notecard()
        req = '{"req":"hub.status"}'
        seq_number = 37

        req_string = card._crc_add(req, seq_number)

        req_json = json.loads(req_string)
        # The format should be SSSS:CCCCCCCC, where S and C are hex digits
        # comprising the sequence number and CRC32, respectively.
        pattern = r'^[0-9A-Fa-f]{4}:[0-9A-Fa-f]{8}$'
        assert re.match(pattern, req_json['crc'])

    # _crc_error tests.
    @pytest.mark.parametrize('crc_supported', [False, True])
    def test_crc_error_handles_lack_of_crc_field_correctly(self, crc_supported):
        card = notecard.Notecard()
        card._card_supports_crc = crc_supported
        rsp_bytes = b'{}\r\n'

        error = card._crc_error(rsp_bytes)

        assert error == crc_supported

    def test_crc_error_returns_error_if_sequence_number_int_conversion_fails(
            self):
        card = notecard.Notecard()
        # Sequence number is invalid hex.
        rsp_bytes = b'{"crc":"000Z:A3A6BF43"}\r\n'

        error = card._crc_error(rsp_bytes)

        assert error

    def test_crc_error_returns_error_if_crc_int_conversion_fails(self):
        card = notecard.Notecard()
        # CRC is invalid hex.
        rsp_bytes = b'{"crc":"0001:A3A6BF4Z"}\r\n'

        error = card._crc_error(rsp_bytes)

        assert error

    def test_crc_error_returns_error_if_sequence_number_wrong(self):
        card = notecard.Notecard()
        seq_number = 37
        card._last_request_seq_number = seq_number
        # Sequence number should be 37 (0x25), but the response has 38 (0x26).
        rsp_bytes = b'{"crc":"0026:A3A6BF43"}\r\n'

        error = card._crc_error(rsp_bytes)

        assert error

    def test_crc_error_returns_error_if_crc_wrong(self):
        card = notecard.Notecard()
        seq_number = 37
        card._last_request_seq_number = seq_number
        # CRC should be A3A6BF43.
        rsp_bytes = b'{"crc":"0025:A3A6BF44"}\r\n'

        error = card._crc_error(rsp_bytes)

        assert error

    @pytest.mark.parametrize(
        'rsp_bytes',
        [
            # Without CRC, the response is {}.
            b'{"crc":"002A:A3A6BF43"}\r\n',
            # Make sure case of sequence number hex doesn't matter.
            b'{"crc":"002a:A3A6BF43"}\r\n',
            # Make sure case of CRC hex doesn't matter.
            b'{"crc":"002A:a3a6bf43"}\r\n',
            # Without CRC, the response is {"connected": true}. This makes sure
            # _crc_error handles the "," between the two fields properly.
            b'{"connected": true,"crc": "002A:025A2457"}\r\n',
        ]
    )
    def test_crc_error_returns_no_error_if_sequence_number_and_crc_ok(
            self, rsp_bytes):
        card = notecard.Notecard()
        seq_number = 42
        card._last_request_seq_number = seq_number

        error = card._crc_error(rsp_bytes)

        assert not error

    # Transaction tests.
    def arrange_transaction_test(self):
        card = notecard.Notecard()
        card.Reset = MagicMock()
        card.lock = MagicMock()
        card.unlock = MagicMock()
        card._transact = MagicMock(return_value=b'{}\r\n')
        card._crc_error = MagicMock(return_value=False)

        return card

    @pytest.mark.parametrize('reset_required', [False, True])
    def test_transaction_calls_reset_if_needed(
            self, arrange_transaction_test, reset_required):
        card = arrange_transaction_test()
        card._reset_required = reset_required
        req = {"req": "hub.status"}

        card.Transaction(req)

        if reset_required:
            card.Reset.assert_called_once()
        else:
            card.Reset.assert_not_called()

    @pytest.mark.parametrize('lock', [False, True])
    def test_transaction_handles_locking_correctly(
            self, arrange_transaction_test, lock):
        card = arrange_transaction_test()
        req = {"req": "hub.status"}

        card.Transaction(req, lock=lock)

        if lock:
            card.lock.assert_called_once()
            card.unlock.assert_called_once()
        else:
            card.lock.assert_not_called()
            card.unlock.assert_not_called()

    @pytest.mark.parametrize('lock', [False, True])
    def test_transaction_handles_locking_after_exception_correctly(
            self, arrange_transaction_test, lock):
        card = arrange_transaction_test()
        card._transact.side_effect = Exception('_transact failed.')
        req = {"req": "hub.status"}

        with pytest.raises(Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req, lock=lock)

        if lock:
            card.lock.assert_called_once()
            card.unlock.assert_called_once()
        else:
            card.lock.assert_not_called()
            card.unlock.assert_not_called()

    def test_transaction_calls_txn_manager_start_and_stop(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._transaction_manager = MagicMock()
        req = {"req": "hub.status"}

        card.Transaction(req)

        card._transaction_manager.start.assert_called_once()
        card._transaction_manager.stop.assert_called_once()

    def test_transaction_calls_txn_manager_stop_after_exception(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._transaction_manager = MagicMock()
        card._transact.side_effect = Exception('_transact failed.')
        req = {"req": "hub.status"}

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        card._transaction_manager.start.assert_called_once()
        card._transaction_manager.stop.assert_called_once()

    def test_transaction_calls_reset_if_transact_fails(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._reset_required = False
        card._transact.side_effect = Exception('_transact failed.')
        req = {"req": "hub.status"}

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        card.Reset.assert_called()

    def test_transaction_retries_on_transact_error(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._transact.side_effect = Exception('_transact failed.')
        req = {"req": "hub.status"}

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        assert card._transact.call_count == \
               notecard.CARD_TRANSACTION_RETRIES

    def test_transaction_retries_on_crc_error(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._crc_error.return_value = True
        req = {"req": "hub.status"}

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        assert card._transact.call_count == \
               notecard.CARD_TRANSACTION_RETRIES

    def test_transaction_retries_on_failure_to_parse_json_response(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        req = {"req": "hub.status"}

        with patch('notecard.notecard.json.loads',
                   side_effect=Exception('json.loads failed.')):
            with pytest.raises(
                    Exception, match='Failed to transact with Notecard.'):
                card.Transaction(req)

            assert card._transact.call_count == \
                   notecard.CARD_TRANSACTION_RETRIES

    def test_transaction_retries_on_io_error_in_response(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        req = {"req": "hub.status"}

        with patch('notecard.notecard.json.loads',
                   return_value={'err': 'some {io} error'}):
            with pytest.raises(
                    Exception, match='Failed to transact with Notecard.'):
                card.Transaction(req)

            assert card._transact.call_count == \
                   notecard.CARD_TRANSACTION_RETRIES

    def test_transaction_does_not_retry_on_not_supported_error_in_response(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        req = {"req": "hub.status"}

        with patch('notecard.notecard.json.loads',
                   return_value={'err': 'some error {io} {not-supported}'}):
            card.Transaction(req)
            assert card._transact.call_count == 1

    def test_transaction_does_not_retry_on_bad_bin_error_in_response(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        req = {"req": "hub.status"}

        with patch('notecard.notecard.json.loads',
                   return_value={'err': 'a {bad-bin} error'}):
            with pytest.raises(
                    Exception, match='Failed to transact with Notecard.'):
                card.Transaction(req)

            assert card._transact.call_count == 1

    @pytest.mark.parametrize(
        'rsp_expected,return_type',
        [
            (False, type(None)),
            (True, dict)
        ]
    )
    def test_transaction_returns_proper_type(
            self, rsp_expected, return_type, arrange_transaction_test):
        card = arrange_transaction_test()
        req = {"req": "hub.status"}
        req_bytes = json.dumps(req).encode('utf-8')
        card._prepare_request = MagicMock(
            return_value=(req_bytes, rsp_expected))

        rsp_json = card.Transaction(req)

        assert isinstance(rsp_json, return_type)

    def test_transaction_does_not_retry_if_transact_fails_and_no_response_expected(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._transact.side_effect = Exception('_transact failed.')
        req = {"req": "hub.status"}
        req_bytes = json.dumps(req).encode('utf-8')
        card._prepare_request = MagicMock(return_value=(req_bytes, False))

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        card._transact.assert_called_once()

    @pytest.mark.parametrize('rsp_expected', [False, True])
    def test_transaction_increments_sequence_number_on_success(
            self, rsp_expected, arrange_transaction_test):
        card = arrange_transaction_test()
        seq_number_before = card._last_request_seq_number
        req = {"req": "hub.status"}
        req_bytes = json.dumps(req).encode('utf-8')
        card._prepare_request = MagicMock(
            return_value=(req_bytes, rsp_expected))

        card.Transaction(req)

        seq_number_after = card._last_request_seq_number
        assert seq_number_after == seq_number_before + 1

    @pytest.mark.parametrize('rsp_expected', [False, True])
    def test_transaction_increments_sequence_number_after_exception(
            self, rsp_expected, arrange_transaction_test):
        card = arrange_transaction_test()
        seq_number_before = card._last_request_seq_number
        req = {"req": "hub.status"}
        req_bytes = json.dumps(req).encode('utf-8')
        card._prepare_request = MagicMock(
            return_value=(req_bytes, rsp_expected))
        card._transact.side_effect = Exception('_transact failed.')

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        seq_number_after = card._last_request_seq_number
        assert seq_number_after == seq_number_before + 1

    def test_transaction_queues_up_a_reset_on_error(
            self, arrange_transaction_test):
        card = arrange_transaction_test()
        card._reset_required = False
        card._transact.side_effect = Exception('_transact failed.')
        req = {"req": "hub.status"}

        with pytest.raises(
                Exception, match='Failed to transact with Notecard.'):
            card.Transaction(req)

        assert card._reset_required

    # Command tests.
    def test_command_returns_none(self):
        card = notecard.Notecard()
        card.Transaction = MagicMock()

        rsp = card.Command({'cmd': 'hub.set'})

        # A command generates no response, by definition.
        assert rsp is None

    def test_command_fails_if_given_req(self):
        card = notecard.Notecard()

        # Can't issue a command with 'req', must use 'cmd'.
        with pytest.raises(Exception):
            card.Command({'req': 'card.sleep'})

    # UserAgentSent tests.
    def test_user_agent_not_sent_before_hub_set(self):
        card = notecard.Notecard()

        assert not card.UserAgentSent()

    @pytest.mark.parametrize(
        'request_method,request_key',
        [
            ('Transaction', 'req'),
            ('Command', 'cmd')
        ]
    )
    def test_user_agent_sent_after_hub_set(self, arrange_transaction_test,
                                           request_method, request_key):
        card = arrange_transaction_test()

        req = dict()
        req[request_key] = 'hub.set'
        method = getattr(card, request_method)
        method(req)

        assert card.UserAgentSent()

    # GetUserAgent tests.
    def test_get_user_agent(self):
        card = notecard.Notecard()
        userAgent = card.GetUserAgent()

        assert userAgent['agent'] == 'note-python'
        assert userAgent['os_name'] is not None
        assert userAgent['os_platform'] is not None
        assert userAgent['os_version'] is not None
        assert userAgent['os_family'] is not None

    # SetAppUserAgent tests.
    def set_user_agent_info(self, info=None):
        card = notecard.Notecard()
        req = {"req": "hub.set"}
        card.SetAppUserAgent(info)
        req = json.loads(card._prepare_request(req)[0])
        return req

    def test_set_app_user_agent_amends_hub_set_request(self):
        req = self.set_user_agent_info()

        assert req['body'] is not None

    def test_set_app_user_agent_adds_app_info_to_hub_set_request(self):
        info = {"app": "myapp"}

        req = self.set_user_agent_info(info)

        assert req['body']['app'] == 'myapp'
