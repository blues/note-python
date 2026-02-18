"""High-speed binary file upload to Notehub via the Notecard."""

import sys
import time

from notecard.cobs import cobs_encode
from notecard.notecard import Notecard

if sys.implementation.name == 'cpython':
    import hashlib

    def _md5_hash(data):
        """Create an MD5 digest of the given data."""
        return hashlib.md5(data).hexdigest()
else:
    from .md5 import digest as _md5_hash

BINARY_STAGE_RETRIES = 50
WEB_POST_RETRIES = 20
WEB_POST_RETRY_DELAY_SECS = 15

try:
    _monotonic = time.monotonic
except AttributeError:
    _monotonic = time.time


def _stage_binary_chunk(card, chunk_data):
    """Stage a binary chunk into the Notecard's binary buffer.

    Performs card.binary.put + raw byte transmit + verification, with
    retries on failure. Mirrors the Go implementation's inner binary
    transfer retry loop.

    Args:
        card (Notecard): The Notecard object.
        chunk_data (bytearray): The raw chunk data to stage.

    Raises:
        Exception: If staging fails after all retries.
    """
    encoded = cobs_encode(bytearray(chunk_data), ord('\n'))
    req = {
        'req': 'card.binary.put',
        'cobs': len(encoded),
    }
    encoded.append(ord('\n'))
    expected_len = len(chunk_data)

    tries_left = BINARY_STAGE_RETRIES
    while tries_left > 0:
        try:
            card.lock()
            rsp = card.Transaction(req, lock=False)
            if 'err' in rsp:
                raise Exception(rsp['err'])
            card.transmit(encoded, delay=False)
        except Exception:
            tries_left -= 1
            if tries_left == 0:
                raise
            continue
        finally:
            card.unlock()

        try:
            rsp = card.Transaction({'req': 'card.binary'})
        except Exception:
            tries_left -= 1
            if tries_left == 0:
                raise
            continue

        if 'err' in rsp:
            err_msg = rsp['err']
            if '{bad-bin}' in err_msg or '{io}' in err_msg:
                tries_left -= 1
                if tries_left == 0:
                    raise Exception(
                        f'Failed to stage binary data: {err_msg}')
                continue
            raise Exception(f'Failed to stage binary data: {err_msg}')

        actual_len = rsp.get('length', 0)
        if actual_len != expected_len:
            tries_left -= 1
            if tries_left == 0:
                raise Exception(
                    f'Binary length mismatch: expected {expected_len}, '
                    f'got {actual_len}.')
            continue

        return

    raise Exception('Failed to stage binary data after retries.')


def upload(card, data, route, target=None, label=None,
           content_type='application/octet-stream', max_chunk_size=0,
           progress_cb=None):
    """Upload binary data to a Notehub proxy route via the Notecard.

    The data is chunked to fit in the Notecard's binary buffer, staged
    via card.binary.put, and sent to Notehub via web.post with
    binary:true.

    Args:
        card (Notecard): The Notecard object.
        data (bytes or bytearray): The binary data to upload.
        route (str): The Notehub proxy route alias.
        target (str, optional): URL path appended to the route (sent as
            ``name`` in the web.post request).
        label (str, optional): Filename label for the upload.
        content_type (str): MIME type. Default ``application/octet-stream``.
        max_chunk_size (int): Maximum chunk size in bytes. 0 means use the
            Notecard's maximum buffer capacity.
        progress_cb (callable, optional): Called after each chunk with a dict
            containing progress information.

    Returns:
        dict: Upload statistics with keys ``bytes_uploaded``, ``chunks``,
        ``duration_secs``, and ``bytes_per_sec``.

    Raises:
        ValueError: If ``route`` is empty or ``data`` is empty.
        Exception: If the upload fails.
    """
    if not route:
        raise ValueError('route must not be empty.')
    if not data:
        raise ValueError('data must not be empty.')

    rsp = card.Transaction({'req': 'card.binary', 'reset': True})
    if 'err' in rsp and '{bad-bin}' not in rsp['err']:
        raise Exception(
            f'Error querying card.binary: {rsp["err"]}')

    buf_capacity = rsp.get('max', 0)
    if buf_capacity == 0:
        raise Exception(
            'Notecard binary buffer capacity is zero or not reported.')

    if max_chunk_size > 0:
        chunk_size = min(max_chunk_size, buf_capacity)
    else:
        chunk_size = buf_capacity

    total_len = len(data)
    total_chunks = (total_len + chunk_size - 1) // chunk_size
    upload_start = _monotonic()
    bytes_sent = 0

    for chunk_idx in range(total_chunks):
        offset = chunk_idx * chunk_size
        end = min(offset + chunk_size, total_len)
        chunk_data = data[offset:end]
        chunk_len = len(chunk_data)
        chunk_md5 = _md5_hash(chunk_data)

        _stage_binary_chunk(card, chunk_data)

        web_req = {
            'req': 'web.post',
            'route': route,
            'binary': True,
            'content': content_type,
            'offset': offset,
            'status': chunk_md5,
        }
        if target:
            web_req['name'] = target
        if label:
            web_req['label'] = label
        # Only set total for multi-chunk (segmented) uploads, matching
        # the Go implementation. This tells Notehub to expect multiple
        # segments and reassemble them.
        if total_chunks > 1:
            web_req['total'] = total_len

        web_tries = WEB_POST_RETRIES
        while web_tries > 0:
            rsp = card.Transaction(web_req)
            result_code = rsp.get('result', 0)
            if result_code >= 300 or 'err' in rsp:
                web_tries -= 1
                if web_tries == 0:
                    err_detail = rsp.get('err', f'HTTP {result_code}')
                    raise Exception(
                        f'web.post failed after retries: {err_detail}')
                time.sleep(WEB_POST_RETRY_DELAY_SECS)
                _stage_binary_chunk(card, chunk_data)
                continue
            break

        bytes_sent += chunk_len
        elapsed = _monotonic() - upload_start
        current_bps = chunk_len / elapsed if elapsed > 0 else 0
        avg_bps = bytes_sent / elapsed if elapsed > 0 else 0
        remaining = total_len - bytes_sent
        eta = remaining / avg_bps if avg_bps > 0 else 0

        if progress_cb:
            progress_cb({
                'chunk': chunk_idx + 1,
                'total_chunks': total_chunks,
                'bytes_sent': bytes_sent,
                'total_bytes': total_len,
                'percent_complete': (bytes_sent / total_len) * 100,
                'bytes_per_sec': current_bps,
                'avg_bytes_per_sec': avg_bps,
                'eta_secs': eta,
            })

    duration = _monotonic() - upload_start
    return {
        'bytes_uploaded': bytes_sent,
        'chunks': total_chunks,
        'duration_secs': duration,
        'bytes_per_sec': bytes_sent / duration if duration > 0 else 0,
    }
