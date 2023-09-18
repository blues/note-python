"""Module for computing the CRC32 of arbitrary data."""

crc32_lookup_table = [
    0x00000000, 0x1DB71064, 0x3B6E20C8, 0x26D930AC, 0x76DC4190, 0x6B6B51F4,
    0x4DB26158, 0x5005713C, 0xEDB88320, 0xF00F9344, 0xD6D6A3E8, 0xCB61B38C,
    0x9B64C2B0, 0x86D3D2D4, 0xA00AE278, 0xBDBDF21C
]


def _logical_rshift(val, shift_amount, num_bits=32):
    """Logcally right shift `val` by `shift_amount` bits.

    Logical right shift (i.e. right shift that fills with 0s instead of the
    sign bit) isn't supported natively in Python. This is a simple
    implementation. See:
    https://realpython.com/python-bitwise-operators/#arithmetic-vs-logical-shift
    """
    unsigned_val = val % (1 << num_bits)
    return unsigned_val >> shift_amount


def crc32(data):
    """Compute CRC32 of the given data.

    Small lookup-table half-byte CRC32 algorithm based on:
    https://create.stephan-brumme.com/crc32/#half-byte
    """
    crc = ~0
    for idx in range(len(data)):
        crc = crc32_lookup_table[(crc ^ data[idx]) & 0x0F] ^ _logical_rshift(crc, 4)
        crc = crc32_lookup_table[(crc ^ _logical_rshift(data[idx], 4)) & 0x0F] ^ _logical_rshift(crc, 4)

    return ~crc & 0xffffffff
