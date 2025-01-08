"""Helper methods for doing binary transfers to/from a Notecard."""

import sys
from notecard.cobs import cobs_encode, cobs_decode
from notecard.notecard import Notecard, CARD_INTRA_TRANSACTION_TIMEOUT_SEC

BINARY_RETRIES = 2

if sys.implementation.name == 'cpython':
    import hashlib

    def _md5_hash(data):
        """Create an MD5 digest of the given data."""
        return hashlib.md5(data).hexdigest()
else:
    from .md5 import digest as _md5_hash


def binary_store_decoded_length(card: Notecard):
    """Get the length of the decoded binary data store."""
    rsp = card.Transaction({'req': 'card.binary'})
    # Ignore {bad-bin} errors, but fail on other types of errors.
    if 'err' in rsp and '{bad-bin}' not in rsp['err']:
        raise Exception(
            f'Error in response to card.binary request: {rsp["err"]}.')

    return rsp['length'] if 'length' in rsp else 0


def binary_store_reset(card: Notecard):
    """Reset the binary data store."""
    rsp = card.Transaction({'req': 'card.binary', 'delete': True})
    if 'err' in rsp:
        raise Exception(
            f'Error in response to card.binary delete request: {rsp["err"]}.')


def binary_store_transmit(card: Notecard, data: bytearray, offset: int):
    """Write bytes to index `offset` of the binary data store."""
    # Make a copy of the data to transmit. We do not modify the user's passed in
    # `data` object.
    tx_data = bytearray(data)
    rsp = card.Transaction({'req': 'card.binary'})

    # Ignore `{bad-bin}` errors, because we intend to overwrite the data.
    if 'err' in rsp and '{bad-bin}' not in rsp['err']:
        raise Exception(rsp['err'])

    if 'max' not in rsp or rsp['max'] == 0:
        raise Exception(('Unexpected card.binary response: max is zero or not '
                         'present.'))

    curr_len = rsp['length'] if 'length' in rsp else 0
    if offset != curr_len:
        raise Exception('Notecard data length is misaligned with offset.')

    max_len = rsp['max']
    remaining = max_len - curr_len if offset > 0 else max_len
    if len(tx_data) > remaining:
        raise Exception(('Data to transmit won\'t fit in the Notecard\'s binary'
                         ' store.'))

    encoded = cobs_encode(tx_data, ord('\n'))
    req = {
        'req': 'card.binary.put',
        'cobs': len(encoded),
        'status': _md5_hash(tx_data)
    }
    encoded.append(ord('\n'))
    if offset > 0:
        req['offset'] = offset

    tries = 1 + BINARY_RETRIES
    while tries > 0:
        try:
            # We need to hold the lock for both the card.binary.put transaction
            # and the subsequent transmission of the binary data.
            card.lock()

            # Pass lock=false because we're already locked.
            rsp = card.Transaction(req, lock=False)
            if 'err' in rsp:
                raise Exception(rsp['err'])

            # Send the binary data.
            card.transmit(encoded, delay=False)
        finally:
            card.unlock()

        rsp = card.Transaction({'req': 'card.binary'})
        if 'err' in rsp:
            # Retry on {bad-bin} errors.
            if '{bad-bin}' in rsp['err']:
                tries -= 1

                if card._debug and tries > 0:
                    print('Error during binary transmission, retrying...')
            # Fail on all other error types.
            else:
                raise Exception(rsp['err'])
        else:
            break

    if tries == 0:
        raise Exception('Failed to transmit binary data.')


def binary_store_receive(card, offset: int, length: int):
    """Receive `length' bytes from index `offset` of the binary data store."""
    req = {
        'req': 'card.binary.get',
        'offset': offset,
        'length': length
    }
    try:
        # We need to hold the lock for both the card.binary.get transaction
        # and the subsequent receipt of the binary data.
        card.lock()

        # Pass lock=false because we're already locked.
        rsp = card.Transaction(req, lock=False)
        if 'err' in rsp:
            raise Exception(rsp['err'])

        # Receive the binary data, keeping everything except the last byte,
        # which is a newline.
        try:
            encoded = card.receive(delay=False)[:-1]
        except Exception as e:
            # Queue up a reset if there was an issue receiving the binary data.
            # The reset will attempt to drain the binary data from the Notecard
            # so that the comms channel with the Notecard is clean before the
            # next transaction.
            card._reset_required = True
            raise e

    finally:
        card.unlock()

    decoded = cobs_decode(encoded, ord('\n'))

    if _md5_hash(decoded) != rsp['status']:
        raise Exception('Computed MD5 does not match received MD5.')

    return decoded
