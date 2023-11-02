"""Methods for COBS encoding and decoding arbitrary bytearrays."""


def cobs_encode(data: bytearray, eop: int) -> bytearray:
    """COBS encode an array of bytes, using eop as the end of packet marker."""
    cobs_overhead = 1 + (len(data) // 254)
    encoded = bytearray(len(data) + cobs_overhead)
    code = 1
    idx = 0
    code_idx = idx
    idx += 1

    for byte in data:
        if byte != 0:
            encoded[idx] = byte ^ eop
            idx += 1
            code += 1
        if byte == 0 or code == 0xFF:
            encoded[code_idx] = code ^ eop
            code = 1
            code_idx = idx
            idx += 1

    encoded[code_idx] = code ^ eop

    return encoded[:idx]


def cobs_decode(encoded: bytes, eop: int) -> bytearray:
    """COBS decode an array of bytes, using eop as the end of packet marker."""
    decoded = bytearray(len(encoded))
    idx = 0
    copy = 0
    code = 0xFF

    for byte in encoded:
        if copy != 0:
            decoded[idx] = byte ^ eop
            idx += 1
        else:
            if code != 0xFF:
                decoded[idx] = 0
                idx += 1

            copy = byte ^ eop
            code = copy

            if code == 0:
                break

        copy -= 1

    return decoded[:idx]
