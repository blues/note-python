import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402
from notecard.cobs import cobs_encode  # noqa: E402
from notecard.binary_helpers import (  # noqa: E402
    binary_store_decoded_length,
    binary_store_reset,
    binary_store_receive,
    binary_store_transmit,
    _md5_hash,
    BINARY_RETRIES
)


@pytest.fixture
def arrange_test():
    def _arrange_test():
        card = notecard.Notecard()
        card.Transaction = MagicMock()
        card.lock = MagicMock()
        card.unlock = MagicMock()

        return card

    yield _arrange_test


@pytest.fixture
def arrange_rx_test(arrange_test):
    def _arrange_rx_test(bad_md5=False):
        card = arrange_test()

        # Set up receive.
        rx_data = bytearray.fromhex('deadbeef0a')
        card.receive = MagicMock(return_value=rx_data)

        # Set up Transaction.
        if bad_md5:
            rsp = {'status': 'abc'}
        else:
            # This is the MD5 of 0xdeadbeef. Note that 0x0a is omitted -- that's
            # the newline that terminates the binary payload. It isn't included
            # in the MD5 calculation.
            rsp = {'status': '2f249230a8e7c2bf6005ccd2679259ec'}
        card.Transaction.return_value = rsp

        # Don't actually do any COBS decoding. Just return the received data.
        # data minus the newline.
        notecard.binary_helpers.cobs_decode = MagicMock(
            return_value=rx_data[:-1])

        return card

    yield _arrange_rx_test


@pytest.fixture
def arrange_tx_test(arrange_test):
    def _arrange_tx_test(transmit_exception=None, **kwargs):
        card = arrange_test()
        card.transmit = MagicMock()

        CARD_BINARY_PRE_TRANSMIT = 0
        CARD_BINARY_PUT = 1
        CARD_BINARY_POST_TRANSMIT = 2
        DONE = 3

        class TransactionSideEffect:
            '''Iterable for the Transaction method that uses a state machine for
               various binary_store_transmit scenarios exercised in these unit
               tests.'''
            def __init__(self, pre_transmit_err=None, maximum=1024, length=0,
                         card_binary_put_err=None,
                         card_binary_put_exception=None, post_transmit_err=None,
                         retry_transmit_forever=False):
                # 'err' field value in the pre-transmission card.binary
                # response.
                self.pre_transmit_err = pre_transmit_err
                # 'max' field value in the pre-transmission card.binary
                # response.
                self.maximum = maximum
                # 'length' field value in the pre-transmission card.binary
                # response.
                self.length = length
                # 'err' field value in the card.binary.put response.
                self.card_binary_put_err = card_binary_put_err
                # Raise an exception on the card.binary.put request, using the
                # string `card_binary_put_exception`.
                self.card_binary_put_exception = card_binary_put_exception
                # 'err' field value in the post-transmission card.binary
                # response.
                self.post_transmit_err = post_transmit_err
                # If this is true, post_transmit_err will not be cleared on a
                # transmission retry. This results in continuous retrying.
                self.retry_transmit_forever = retry_transmit_forever

            def __iter__(self):
                self.state = CARD_BINARY_PRE_TRANSMIT

            def __next__(self):
                # This is the aforementioned state machine. The first
                # Transaction call in binary_store_transmit is a card.binary
                # request.
                if self.state == CARD_BINARY_PRE_TRANSMIT:
                    rsp = {'length': self.length}
                    if self.maximum:
                        rsp['max'] = self.maximum
                    if self.pre_transmit_err:
                        rsp['err'] = self.pre_transmit_err
                    self.state = CARD_BINARY_PUT

                # The second call is card.binary.put.
                elif self.state == CARD_BINARY_PUT:
                    if self.card_binary_put_exception:
                        rsp = Exception(self.card_binary_put_exception)
                    elif self.card_binary_put_err:
                        rsp = {'err': self.card_binary_put_err}
                    else:
                        rsp = {}
                    self.state = CARD_BINARY_POST_TRANSMIT

                # The third call is card.binary again.
                elif self.state == CARD_BINARY_POST_TRANSMIT:
                    if self.post_transmit_err:
                        rsp = {'err': self.post_transmit_err}
                        # Unless we intend to error out on the post transmission
                        # card.binary continuously, clear the error here so that
                        # we don't hit it again on the retry.
                        if not self.retry_transmit_forever:
                            self.post_transmit_err = None

                        self.state = CARD_BINARY_PUT
                    else:
                        rsp = {}
                        self.state = DONE

                elif self.state == DONE:
                    raise StopIteration

                return rsp

        card.Transaction.side_effect = TransactionSideEffect(**kwargs)

        if transmit_exception:
            card.transmit.side_effect = Exception(transmit_exception)

        return card

    with patch('notecard.binary_helpers.cobs_encode', side_effect=cobs_encode):
        yield _arrange_tx_test


@pytest.fixture
def tx_data():
    return bytearray.fromhex(('82f9a19b7e02c95bd87b38a8ce479608830ee68ffe4d1763'
                              'ecc205681ed537a3'))


def get_card_binary_put_call(card):
    '''Find the card.binary.put request by searching through the calls to
       card.Transaction.'''
    card_binary_put_call = None
    for call in card.Transaction.call_args_list:
        req = call[0][0]
        if req['req'] == 'card.binary.put':
            card_binary_put_call = call
            break

    return card_binary_put_call


class TestBinaryStoreDecodedLength:
    # binary_store_decoded_length tests.
    def test_makes_card_binary_request(self, arrange_test):
        card = arrange_test()

        binary_store_decoded_length(card)

        card.Transaction.assert_called_once_with({'req': 'card.binary'})

    def test_returns_zero_if_no_length_field(self, arrange_test):
        card = arrange_test()
        card.Transaction.return_value = {}

        assert binary_store_decoded_length(card) == 0

    def test_returns_length_length_field_present(self, arrange_test):
        card = arrange_test()
        length = 99
        card.Transaction.return_value = {'length': length}

        assert binary_store_decoded_length(card) == length

    def test_ignores_bad_bin_errors(self, arrange_test):
        card = arrange_test()
        card.Transaction.return_value = {'err': '{bad-bin}'}

        binary_store_decoded_length(card)

    def test_raises_exception_on_non_bad_bin_error(self, arrange_test):
        card = arrange_test()
        err_msg = 'some error'
        card.Transaction.return_value = {'err': err_msg}
        exception_msg = f'Error in response to card.binary request: {err_msg}.'

        with pytest.raises(Exception, match=exception_msg):
            binary_store_decoded_length(card)


class TestBinaryStoreReset:
    def test_makes_card_binary_request_with_delete_true(
            self, arrange_test):
        card = arrange_test()

        binary_store_reset(card)

        card.Transaction.assert_called_once_with(
            {'req': 'card.binary', 'delete': True})

    def test_raises_exception_on_error_in_response(self, arrange_test):
        card = arrange_test()
        err_msg = 'some error'
        card.Transaction.return_value = {'err': err_msg}
        exception_msg = ('Error in response to card.binary delete request: '
                         f'{err_msg}.')

        with pytest.raises(Exception, match=exception_msg):
            binary_store_reset(card)


class TestBinaryStoreReceive:
    def test_maps_card_binary_get_params_correctly(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99
        expected_req = {
            'req': 'card.binary.get',
            'offset': offset,
            'length': length
        }

        binary_store_receive(card, offset, length)

        card.Transaction.assert_called_once_with(expected_req, lock=False)

    def test_locks_and_unlocks(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99

        binary_store_receive(card, offset, length)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_unlocks_after_card_binary_get_exception(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99
        exception_msg = 'Transaction failed.'
        card.Transaction.side_effect = Exception(exception_msg)

        with pytest.raises(Exception, match=exception_msg):
            binary_store_receive(card, offset, length)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_unlocks_after_receive_exception(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99
        exception_msg = 'receive failed.'
        card.receive.side_effect = Exception(exception_msg)

        with pytest.raises(Exception, match=exception_msg):
            binary_store_receive(card, offset, length)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_raises_exception_if_error_in_card_binary_get_response(
            self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99
        err_msg = 'some error'
        card.Transaction.return_value['err'] = err_msg

        with pytest.raises(Exception, match=err_msg):
            binary_store_receive(card, offset, length)

    def test_unlocks_if_error_in_card_binary_get_response(
            self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99
        err_msg = 'some error'
        card.Transaction.return_value['err'] = err_msg

        with pytest.raises(Exception, match=err_msg):
            binary_store_receive(card, offset, length)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_queues_reset_after_receive_exception(self, arrange_rx_test):
        card = arrange_rx_test()
        card._reset_required = False
        offset = 11
        length = 99
        exception_msg = 'receive failed.'
        card.receive.side_effect = Exception(exception_msg)

        with pytest.raises(Exception, match=exception_msg):
            binary_store_receive(card, offset, length)

        assert card._reset_required

    def test_raises_exception_on_bad_md5(self, arrange_rx_test):
        card = arrange_rx_test(bad_md5=True)
        offset = 11
        length = 99
        exception_msg = 'Computed MD5 does not match received MD5.'

        with pytest.raises(Exception, match=exception_msg):
            binary_store_receive(card, offset, length)

    def test_calls_cobs_decode_on_rx_data_without_newline(
            self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99

        binary_store_receive(card, offset, length)

        # First, verify what was received ends in a newline.
        assert card.receive.return_value[-1] == ord('\n')
        # Then, check that cobs_decode was called with everything but that
        # newline.
        assert card.receive.return_value[:-1] == \
               notecard.binary_helpers.cobs_decode.call_args[0][0]

    def test_calls_cobs_decode_with_newline_as_eop(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99

        binary_store_receive(card, offset, length)

        assert notecard.binary_helpers.cobs_decode.call_args[0][1] == ord('\n')

    def test_returns_cobs_decoded_data(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99

        data = binary_store_receive(card, offset, length)

        assert notecard.binary_helpers.cobs_decode.return_value == data

    def test_computes_md5_over_cobs_decoded_data(self, arrange_rx_test):
        card = arrange_rx_test()
        offset = 11
        length = 99
        md5_fn = notecard.binary_helpers._md5_hash

        with patch('notecard.binary_helpers._md5_hash',
                   side_effect=md5_fn) as md5_mock:
            binary_store_receive(card, offset, length)

            cobs_decoded_data = \
                notecard.binary_helpers.cobs_decode.call_args[0][0]
            assert md5_mock.call_args[0][0] == cobs_decoded_data


class TestBinaryStoreTransmit:
    def test_ignores_bad_bin_err_on_initial_card_binary_request(
            self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test(pre_transmit_err='{bad-bin}')

        binary_store_transmit(card, tx_data, offset)

    def test_fails_on_non_bad_bin_err_on_initial_card_binary_request(
            self, tx_data, arrange_tx_test):
        offset = 0
        err_msg = 'some error'
        card = arrange_tx_test(pre_transmit_err=err_msg)

        with pytest.raises(Exception, match=err_msg):
            binary_store_transmit(card, tx_data, offset)

    @pytest.mark.parametrize('maximum', [None, 0])
    def test_fails_on_invalid_max_on_initial_card_binary_request(
            self, tx_data, arrange_tx_test, maximum):
        offset = 0
        card = arrange_tx_test(maximum=maximum)
        exception_msg = ('Unexpected card.binary response: max is zero or not '
                         'present.')

        with pytest.raises(Exception, match=exception_msg):
            binary_store_transmit(card, tx_data, offset)

    def test_fails_if_offset_not_equal_to_length_reported_by_notecard(
            self, tx_data, arrange_tx_test):
        offset = 1
        card = arrange_tx_test()
        exception_msg = 'Notecard data length is misaligned with offset.'

        with pytest.raises(Exception, match=exception_msg):
            binary_store_transmit(card, tx_data, offset)

    def test_fails_if_data_length_exceeds_available_space_on_notecard(
            self, tx_data, arrange_tx_test):
        offset = 5
        card = arrange_tx_test(maximum=offset, length=offset)
        exception_msg = ('Data to transmit won\'t fit in the Notecard\'s binary'
                         ' store.')

        with pytest.raises(Exception, match=exception_msg):
            binary_store_transmit(card, tx_data, offset)

    def test_calls_cobs_encode_on_tx_data(self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test()

        binary_store_transmit(card, tx_data, offset)

        assert notecard.binary_helpers.cobs_encode.call_args[0][0] == tx_data

    def test_calls_cobs_encode_with_newline_as_eop(
            self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test()

        binary_store_transmit(card, tx_data, offset)

        assert notecard.binary_helpers.cobs_encode.call_args[0][1] == ord('\n')

    def test_maps_card_binary_put_params_correctly(
            self, tx_data, arrange_tx_test):
        offset = 1
        card = arrange_tx_test(length=offset)

        binary_store_transmit(card, tx_data, offset)

        card_binary_put_call = get_card_binary_put_call(card)
        # If we didn't find a card.binary.put request, something's wrong.
        assert card_binary_put_call is not None

        req = card_binary_put_call[0][0]
        assert req['cobs'] == len(cobs_encode(tx_data, ord('\n')))
        assert req['status'] == _md5_hash(tx_data)
        assert req['offset'] == offset

    def test_sends_card_binary_put_with_lock_false(
            self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test()

        binary_store_transmit(card, tx_data, offset)

        card_binary_put_call = get_card_binary_put_call(card)
        # If we didn't find a card.binary.put request, something's wrong.
        assert card_binary_put_call is not None

        assert not card_binary_put_call[1]['lock']

    def test_calls_transmit_with_delay_false(self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test()

        binary_store_transmit(card, tx_data, offset)

        assert not card.transmit.call_args[1]['delay']

    def test_calls_transmit_with_cobs_encoded_data_plus_newline(
            self, tx_data, arrange_tx_test):
        expected_data = cobs_encode(bytearray(tx_data), ord('\n')) + b'\n'
        offset = 0
        card = arrange_tx_test()

        binary_store_transmit(card, tx_data, offset)

        assert card.transmit.call_args[0][0] == expected_data

    def test_raises_exception_on_card_binary_put_error(
            self, tx_data, arrange_tx_test):
        offset = 0
        err_msg = 'some error'
        card = arrange_tx_test(card_binary_put_err=err_msg)

        with pytest.raises(Exception, match=err_msg):
            binary_store_transmit(card, tx_data, offset)

    def test_locks_and_unlocks(self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test()

        binary_store_transmit(card, tx_data, offset)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_unlocks_after_card_binary_put_exception(
            self, tx_data, arrange_tx_test):
        offset = 0
        exception_msg = 'card.binary.put failed'
        card = arrange_tx_test(
            card_binary_put_exception=exception_msg)

        with pytest.raises(Exception, match=exception_msg):
            binary_store_transmit(card, tx_data, offset)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_unlocks_after_card_binary_put_error(
            self, tx_data, arrange_tx_test):
        offset = 0
        err_msg = 'some error'
        card = arrange_tx_test(card_binary_put_err=err_msg)

        with pytest.raises(Exception, match=err_msg):
            binary_store_transmit(card, tx_data, offset)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_unlocks_after_transmit_exception(self, tx_data, arrange_tx_test):
        offset = 0
        exception_msg = 'transmit failed'
        card = arrange_tx_test(
            transmit_exception=exception_msg)

        with pytest.raises(Exception, match=exception_msg):
            binary_store_transmit(card, tx_data, offset)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_retries_on_bad_bin_error_after_transmit(
            self, tx_data, arrange_tx_test):
        offset = 0
        card = arrange_tx_test(post_transmit_err='{bad-bin}')

        binary_store_transmit(card, tx_data, offset)

        # transmit should've been called once and then retried once due to the
        # {bad-bin} error.
        assert card.transmit.call_count == 2

    def test_fails_on_card_binary_error_after_transmission(
            self, tx_data, arrange_tx_test):
        offset = 0
        err_msg = 'some error'
        card = arrange_tx_test(post_transmit_err=err_msg)

        with pytest.raises(Exception, match=err_msg):
            binary_store_transmit(card, tx_data, offset)

    def test_fails_after_running_out_of_retries(
            self, tx_data, arrange_tx_test):
        offset = 0
        exception_msg = 'Failed to transmit binary data.'
        card = arrange_tx_test(post_transmit_err='{bad-bin}',
                               retry_transmit_forever=True)

        with pytest.raises(Exception, match=exception_msg):
            binary_store_transmit(card, tx_data, offset)

        # transmit should've been called once and then retried BINARY_RETRIES
        # times.
        assert card.transmit.call_count == BINARY_RETRIES + 1
