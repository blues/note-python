import sys
import os
import pytest
import random

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from notecard.cobs import cobs_encode, cobs_decode  # noqa: E402


@pytest.fixture
def test_data():
    data = [
        0x42, 0x15, 0x14, 0x56, 0x4A, 0x79, 0x17, 0xB3, 0x20,
        0x7E, 0x3D, 0x61, 0x4C, 0x93, 0xA3, 0x33, 0xE9, 0x81,
        0xED, 0x37, 0xA8, 0x35, 0x4D, 0xEF, 0xDA, 0x88, 0xC5,
        0x7F, 0x6F, 0xE8, 0x34, 0x38, 0x46, 0x99, 0x9E, 0xCA,
        0x6D, 0x41, 0x85, 0x03, 0xEA, 0x8C, 0x87, 0x30, 0x68,
        0x33, 0x2D, 0x69, 0x72, 0xF6, 0xAC, 0xDA, 0x58, 0x8A,
        0x1C, 0xB6, 0x8F, 0x66, 0x14, 0x3B, 0x8E, 0xB9, 0x6B,
        0x0E, 0x47, 0xC0, 0x96, 0xFE, 0x2B, 0xE0, 0x58, 0xF4,
        0xE0, 0xB7, 0x8D, 0x9C, 0xED, 0xDE, 0x55, 0x31, 0xB6,
        0xB0, 0xAF, 0xB6, 0xBB, 0x3C, 0x3D, 0xC1, 0xFE, 0xAB,
        0xF4, 0xB9, 0xC8, 0x4C, 0xE4, 0xA1, 0x40, 0x1F, 0x82,
        0x21, 0xF5, 0x25, 0x2A, 0xCC, 0xBF, 0x43, 0xAB, 0x53,
        0x11, 0x16, 0x69, 0xDF, 0x34, 0x88, 0xC9, 0x9F, 0x7C,
        0xBD, 0x66, 0xAC, 0x59, 0x22, 0x62, 0x33, 0x1B, 0x4A,
        0xCB, 0x75, 0x2F, 0xBA, 0x10, 0x12, 0x17, 0x43, 0x35,
        0x28, 0xE1, 0x4D, 0xA2, 0xD0, 0xBF, 0xC3, 0x13, 0x2E,
        0xB2, 0x7A, 0x20, 0xAF, 0xD9, 0x9A, 0x0E, 0xBA, 0xDC,
        0x8E, 0x35, 0xD5, 0x53, 0xC7, 0xE8, 0x6B, 0xB4, 0x4F,
        0xC2, 0x97, 0x7F, 0xB5, 0x36, 0x6F, 0x5C, 0x51, 0x3A,
        0x71, 0x85, 0x35, 0x98, 0x4C, 0x66, 0xEE, 0x3E, 0x9B,
        0x3E, 0xD5, 0x66, 0xEA, 0x97, 0xA4, 0xCF, 0x96, 0xE1,
        0x26, 0x24, 0x69, 0xCD, 0x79, 0xEA, 0xD7, 0xF2, 0x70,
        0xD8, 0xD0, 0x59, 0x04, 0xFA, 0xBE, 0x96, 0xB2, 0x72,
        0x1D, 0xA6, 0xC9, 0xD6, 0x2D, 0xA3, 0x7D, 0x3F, 0x54,
        0xD2, 0x4E, 0xDE, 0x78, 0x82, 0x2C, 0x77, 0xD0, 0x33,
        0x04, 0xBD, 0x3B, 0x0F, 0xDC, 0x7A, 0x8D, 0x7A, 0xF6,
        0x1A, 0x3E, 0x09, 0xDC, 0xC1, 0x61, 0x41, 0xBC, 0x74,
        0xD9, 0xD4, 0xCA, 0x30, 0x84, 0x7D, 0x32, 0xDC, 0x10,
        0x61, 0xC1, 0x70, 0x25, 0x82, 0x85, 0xEE, 0x91, 0x8D,
        0x48, 0xCA, 0x40, 0x3F, 0x72, 0xA6, 0xC9, 0x0C, 0x02,
        0x2F, 0x2D, 0xE3, 0xD1, 0x4F, 0x04, 0x4C, 0xEA, 0x84,
        0x99, 0x19, 0xB0, 0x25, 0x3A, 0xA0, 0x9D, 0x82, 0x0E,
        0x0C, 0x33, 0x90, 0x1C, 0x98, 0x25, 0x89, 0x4D, 0xE7,
        0x1B, 0x11, 0xB1, 0x20, 0x55, 0x6C, 0xEA, 0xEC, 0xD4,
        0x19, 0x75, 0xE2, 0xA7, 0xC6, 0x71, 0x61, 0x8C, 0xB6,
        0x71, 0xC6, 0x00, 0x6F, 0x00, 0x8B, 0x7E, 0x8F, 0x7A,
        0xA1, 0xBC, 0xDE, 0x38, 0x2E, 0x22, 0x04, 0x4B, 0x55,
        0x21, 0xA0, 0xE0, 0x3E, 0x14, 0x41, 0x91, 0x33, 0x60,
        0x8B, 0xCE, 0xE4, 0x07, 0xD1, 0xE9, 0x15, 0x60, 0x5D,
        0x76, 0xDC, 0x86, 0x3E, 0xFB, 0xE6, 0x86, 0xE9, 0x69,
        0xA5, 0xC4, 0x5F, 0x62, 0x70, 0x1C, 0x8E, 0x11, 0x74,
        0xD5, 0x7C, 0x29, 0x7F, 0x0B, 0x42, 0x43, 0x4D, 0x73,
        0x73, 0x57, 0xE2, 0x2D, 0x68, 0xC0, 0x57, 0xC9, 0xED,
        0xAF, 0xF9, 0x0B, 0xFD, 0xA0, 0x93, 0x81, 0x01, 0x1C,
        0x01, 0x7A, 0xB2, 0xC2, 0x23, 0x45, 0x22, 0xCD, 0x63,
        0xAC, 0x58, 0x56, 0x0D, 0x7E, 0xFB, 0xF4, 0x27, 0xED,
        0x5B, 0x1C, 0x47, 0x76, 0xBF, 0x14, 0xE7, 0xAF, 0x15,
        0x67, 0x01, 0x02, 0x33, 0x99, 0x95, 0xD2, 0x4E, 0x3E,
        0x8D, 0xB8, 0xFD, 0x93, 0x36, 0xAF, 0x5C, 0x67, 0x41,
        0xF4, 0x17, 0xDF, 0x5C, 0xD0, 0xBC, 0xE0, 0xAA, 0x5F,
        0xD0, 0x5B, 0xBE, 0xBC, 0x02, 0x30, 0x7B, 0x84, 0xC4,
        0x92, 0x5D, 0xE4, 0x30, 0xFD, 0x66, 0x11, 0x43, 0x44,
        0x5F, 0xD7, 0x29, 0x5A, 0x80, 0x6D, 0x7F, 0x4A, 0xC0,
        0x6F, 0xC9, 0x61, 0x93, 0xFD, 0x5F, 0x37, 0xF7, 0x67,
        0x7B, 0xD4, 0x6D, 0x07, 0xE4, 0x5B, 0x3D, 0x5F, 0x89,
        0x12, 0xE7, 0x2D, 0x07, 0x28, 0x37, 0x41, 0x70, 0xD4,
        0x8F, 0x0F, 0xAA, 0xE9, 0xF6, 0x3B, 0x7D, 0x7F
    ]

    return data


class TestCobs:
    def test_encoded_data_does_not_contain_eop(self, test_data):
        # The code below randomly selects 20 elements of test_data and
        # overwrites them with 0x0A. The encoding process, if correct, is
        # guaranteed to eliminate 0x0A from the data if 0x0A is provided as the
        # EOP byte.
        eop = 0x0A
        for idx in random.sample(range(len(test_data)), 20):
            test_data[idx] = eop

        encoded_data = cobs_encode(bytearray(test_data), eop)

        for b in encoded_data:
            assert b != eop

    def test_encoding_overhead_is_consistent(self, test_data):
        # Make sure our unencoded data doesn't contain the byte 0x00.
        for idx, b in enumerate(test_data):
            if b == 0x00:
                test_data[idx] = 0x01

        # The COBS algorithm guarantees that for spans of data not containing
        # any zero bytes, an overhead byte will be added every 254 bytes.
        # There's also an overhead byte that gets added to the beginning of the
        # encoded data, too.
        overhead = 1 + len(test_data) // 254
        eop = 0x0A

        encoded_data = cobs_encode(bytearray(test_data), eop)

        assert len(encoded_data) == (len(test_data) + overhead)

    def test_decode_returns_original_data(self, test_data):
        eop = 0x0A
        input_data = bytearray(test_data)
        encoded_data = cobs_encode(input_data, eop)

        decoded_data = cobs_decode(encoded_data, eop)

        assert input_data == decoded_data

    def test_encode_does_not_mutate_input_data(self, test_data):
        eop = 0x0A
        input_data = bytearray(test_data)
        original_data = input_data[:]  # This slicing ensures we make a copy.

        cobs_encode(input_data, eop)

        assert input_data == original_data

    def test_decode_does_not_mutate_input_data(self, test_data):
        eop = 0x0A
        input_data = cobs_encode(bytearray(test_data), eop)
        original_data = input_data[:]  # This slicing ensures we make a copy.

        cobs_decode(input_data, eop)

        assert input_data == original_data
