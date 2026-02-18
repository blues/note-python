import os
import sys
import pytest
from unittest.mock import MagicMock, patch, call

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import notecard  # noqa: E402
from notecard.upload import (  # noqa: E402
    upload,
    _stage_binary_chunk,
    _md5_hash,
    BINARY_STAGE_RETRIES,
    WEB_POST_RETRIES,
)


@pytest.fixture
def card():
    """Create a mock Notecard with the methods used by upload."""
    c = notecard.Notecard()
    c.Transaction = MagicMock()
    c.lock = MagicMock()
    c.unlock = MagicMock()
    c.transmit = MagicMock()
    return c


@pytest.fixture
def sample_data():
    """A small sample payload for testing."""
    return bytearray(range(64))


class TestUploadValidation:
    def test_raises_on_empty_route(self, card, sample_data):
        with pytest.raises(ValueError, match='route must not be empty'):
            upload(card, sample_data, route='')

    def test_raises_on_none_route(self, card, sample_data):
        with pytest.raises(ValueError, match='route must not be empty'):
            upload(card, sample_data, route=None)

    def test_raises_on_empty_data(self, card):
        with pytest.raises(ValueError, match='data must not be empty'):
            upload(card, b'', route='my-route')

    def test_raises_on_none_data(self, card):
        with pytest.raises(ValueError, match='data must not be empty'):
            upload(card, None, route='my-route')

    def test_raises_on_zero_buffer_capacity(self, card, sample_data):
        card.Transaction.return_value = {'max': 0}
        with pytest.raises(Exception, match='capacity is zero'):
            upload(card, sample_data, route='my-route')


class TestSingleChunkUpload:
    def test_single_chunk_upload(self, card, sample_data):
        """Data fits in one chunk -- one stage + one web.post."""
        buf_max = len(sample_data) + 100

        call_count = [0]

        def transaction_side_effect(req, **kwargs):
            call_count[0] += 1
            r = req.get('req', req.get('cmd', ''))

            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        result = upload(card, sample_data, route='my-route')

        assert result['bytes_uploaded'] == len(sample_data)
        assert result['chunks'] == 1
        assert result['duration_secs'] >= 0
        assert result['bytes_per_sec'] >= 0

    def test_single_chunk_sets_web_post_fields(self, card, sample_data):
        """Verify the web.post request has the correct fields."""
        buf_max = len(sample_data) + 100
        captured_web_req = {}

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                captured_web_req.update(req)
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        upload(card, sample_data, route='my-route', target='/path',
               label='file.bin', content_type='image/png')

        assert captured_web_req['route'] == 'my-route'
        assert captured_web_req['binary'] is True
        assert captured_web_req['name'] == '/path'
        assert captured_web_req['label'] == 'file.bin'
        assert captured_web_req['content'] == 'image/png'
        assert captured_web_req['offset'] == 0
        # total should NOT be set for single-chunk uploads
        assert 'total' not in captured_web_req
        assert captured_web_req['status'] == _md5_hash(sample_data)

    def test_omits_name_and_label_when_not_provided(self, card, sample_data):
        """target and label should be omitted from web.post when None."""
        buf_max = len(sample_data) + 100
        captured_web_req = {}

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                captured_web_req.update(req)
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        upload(card, sample_data, route='my-route')

        assert 'name' not in captured_web_req
        assert 'label' not in captured_web_req


class TestMultiChunkUpload:
    def test_multi_chunk_upload(self, card):
        """Data requires multiple chunks."""
        data = bytearray(range(256)) * 4  # 1024 bytes
        buf_max = 300  # forces ~4 chunks
        chunk_idx = [0]
        expected_chunks = (len(data) + buf_max - 1) // buf_max

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                # Return length matching the current chunk size
                offset = chunk_idx[0] * buf_max
                end = min(offset + buf_max, len(data))
                return {'length': end - offset}
            if r == 'web.post':
                chunk_idx[0] += 1
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        result = upload(card, data, route='my-route')

        assert result['bytes_uploaded'] == len(data)
        assert result['chunks'] == expected_chunks

    def test_sets_total_for_multi_chunk(self, card):
        """total field should be set in web.post for multi-chunk uploads."""
        data = bytearray(range(256)) * 4  # 1024 bytes
        buf_max = 300
        captured_web_reqs = []

        chunk_idx = [0]

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                offset = chunk_idx[0] * buf_max
                end = min(offset + buf_max, len(data))
                return {'length': end - offset}
            if r == 'web.post':
                captured_web_reqs.append(dict(req))
                chunk_idx[0] += 1
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        upload(card, data, route='my-route')

        assert len(captured_web_reqs) > 1
        for web_req in captured_web_reqs:
            assert web_req['total'] == len(data)

    def test_respects_max_chunk_size(self, card):
        """max_chunk_size limits chunk size even when buffer is larger."""
        data = bytearray(100)
        buf_max = 1000
        max_chunk = 30
        expected_chunks = (len(data) + max_chunk - 1) // max_chunk
        web_post_offsets = []

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                # Track the chunk size from the COBS-encoded length hint
                # is not directly the raw size, so we track via web.post
                # offset math instead. Just return success.
                return {}
            if r == 'card.binary':
                # The verification call: we need to return the length of
                # the chunk that was just staged. Compute from the last
                # web.post offset we haven't sent yet.
                chunk_idx = len(web_post_offsets)
                offset = chunk_idx * max_chunk
                end = min(offset + max_chunk, len(data))
                return {'length': end - offset}
            if r == 'web.post':
                web_post_offsets.append(req['offset'])
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        result = upload(card, data, route='r', max_chunk_size=max_chunk)

        assert result['chunks'] == expected_chunks
        assert web_post_offsets == [i * max_chunk
                                    for i in range(expected_chunks)]


class TestStageBinaryRetry:
    def test_retries_on_transmit_exception(self, card):
        """_stage_binary_chunk retries when transmit raises."""
        chunk = bytearray(b'\x01\x02\x03')

        card.Transaction.side_effect = [
            {},   # first card.binary.put
            {},   # second card.binary.put (retry)
            {'length': len(chunk)},  # verification after retry
        ]
        card.transmit.side_effect = [
            Exception('transmit error'),
            None,
        ]

        _stage_binary_chunk(card, chunk)

        assert card.transmit.call_count == 2

    def test_retries_on_verification_error(self, card):
        """_stage_binary_chunk retries when verification has an error."""
        chunk = bytearray(b'\x01\x02\x03')

        card.Transaction.side_effect = [
            {},  # first card.binary.put
            {'err': '{bad-bin}'},  # first verification fails
            {},  # second card.binary.put (retry)
            {'length': len(chunk)},  # second verification ok
        ]

        _stage_binary_chunk(card, chunk)

        assert card.transmit.call_count == 2

    def test_retries_on_length_mismatch(self, card):
        """_stage_binary_chunk retries when verified length doesn't match."""
        chunk = bytearray(b'\x01\x02\x03')

        card.Transaction.side_effect = [
            {},  # first card.binary.put
            {'length': 999},  # first verification: wrong length
            {},  # second card.binary.put (retry)
            {'length': len(chunk)},  # second verification ok
        ]

        _stage_binary_chunk(card, chunk)

        assert card.transmit.call_count == 2

    def test_fails_after_all_retries_exhausted(self, card):
        """_stage_binary_chunk raises after BINARY_STAGE_RETRIES failures."""
        chunk = bytearray(b'\x01\x02\x03')

        # Every verification fails
        side_effects = []
        for _ in range(BINARY_STAGE_RETRIES):
            side_effects.append({})  # card.binary.put
            side_effects.append({'err': '{bad-bin}'})  # verification
        card.Transaction.side_effect = side_effects

        with pytest.raises(Exception, match='Failed to stage binary data'):
            _stage_binary_chunk(card, chunk)

    def test_locks_and_unlocks_on_each_attempt(self, card):
        """lock/unlock called for each staging attempt."""
        chunk = bytearray(b'\x01\x02\x03')

        card.Transaction.side_effect = [
            {},  # card.binary.put
            {'length': len(chunk)},  # verification
        ]

        _stage_binary_chunk(card, chunk)

        card.lock.assert_called_once()
        card.unlock.assert_called_once()

    def test_unlocks_even_on_exception(self, card):
        """unlock is called even when transmit raises."""
        chunk = bytearray(b'\x01\x02\x03')

        card.Transaction.return_value = {}
        card.transmit.side_effect = Exception('fail')

        with pytest.raises(Exception):
            # Set retries to 1 via patching to avoid long test
            with patch('notecard.upload.BINARY_STAGE_RETRIES', 1):
                _stage_binary_chunk(card, chunk)

        assert card.unlock.call_count >= 1


class TestWebPostRetry:
    @patch('notecard.upload.WEB_POST_RETRY_DELAY_SECS', 0)
    def test_retries_on_http_error(self, card, sample_data):
        """web.post is retried when result >= 300."""
        buf_max = len(sample_data) + 100
        web_post_count = [0]

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                web_post_count[0] += 1
                if web_post_count[0] == 1:
                    return {'result': 500}
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        result = upload(card, sample_data, route='my-route')

        assert web_post_count[0] == 2
        assert result['bytes_uploaded'] == len(sample_data)

    @patch('notecard.upload.WEB_POST_RETRY_DELAY_SECS', 0)
    def test_retries_on_web_post_err(self, card, sample_data):
        """web.post is retried when response has 'err' field."""
        buf_max = len(sample_data) + 100
        web_post_count = [0]

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                web_post_count[0] += 1
                if web_post_count[0] == 1:
                    return {'err': 'some network error'}
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        upload(card, sample_data, route='my-route')

        assert web_post_count[0] == 2

    @patch('notecard.upload.WEB_POST_RETRY_DELAY_SECS', 0)
    @patch('notecard.upload.WEB_POST_RETRIES', 2)
    def test_fails_after_web_post_retries_exhausted(self, card, sample_data):
        """upload raises after WEB_POST_RETRIES web.post failures."""
        buf_max = len(sample_data) + 100

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                return {'result': 500}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        with pytest.raises(Exception, match='web.post failed after retries'):
            upload(card, sample_data, route='my-route')

    @patch('notecard.upload.WEB_POST_RETRY_DELAY_SECS', 0)
    def test_re_stages_binary_on_web_post_retry(self, card, sample_data):
        """Binary data is re-staged before each web.post retry."""
        buf_max = len(sample_data) + 100
        web_post_count = [0]
        binary_put_count = [0]

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                binary_put_count[0] += 1
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                web_post_count[0] += 1
                if web_post_count[0] == 1:
                    return {'result': 500}
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        upload(card, sample_data, route='my-route')

        # Initial stage + re-stage for the retry
        assert binary_put_count[0] == 2


class TestProgressCallback:
    def test_progress_callback_called_per_chunk(self, card):
        """progress_cb is called once per chunk with correct fields."""
        data = bytearray(100)
        buf_max = 40
        expected_chunks = (len(data) + buf_max - 1) // buf_max
        progress_calls = []
        chunk_idx = [0]

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                offset = chunk_idx[0] * buf_max
                end = min(offset + buf_max, len(data))
                return {'length': end - offset}
            if r == 'web.post':
                chunk_idx[0] += 1
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        def progress_cb(info):
            progress_calls.append(info)

        upload(card, data, route='my-route', progress_cb=progress_cb)

        assert len(progress_calls) == expected_chunks

        # Verify first callback
        first = progress_calls[0]
        assert first['chunk'] == 1
        assert first['total_chunks'] == expected_chunks
        assert first['total_bytes'] == len(data)
        assert 'bytes_sent' in first
        assert 'percent_complete' in first
        assert 'bytes_per_sec' in first
        assert 'avg_bytes_per_sec' in first
        assert 'eta_secs' in first

        # Verify last callback
        last = progress_calls[-1]
        assert last['chunk'] == expected_chunks
        assert last['bytes_sent'] == len(data)
        assert last['percent_complete'] == 100.0

    def test_no_error_when_progress_callback_is_none(self, card, sample_data):
        """Upload works fine with no progress callback."""
        buf_max = len(sample_data) + 100

        def transaction_side_effect(req, **kwargs):
            r = req.get('req', '')
            if r == 'card.binary' and req.get('reset'):
                return {'max': buf_max}
            if r == 'card.binary.put':
                return {}
            if r == 'card.binary':
                return {'length': len(sample_data)}
            if r == 'web.post':
                return {'result': 200}
            return {}

        card.Transaction.side_effect = transaction_side_effect

        upload(card, sample_data, route='my-route',
               progress_cb=None)
