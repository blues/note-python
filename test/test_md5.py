import unittest
import sys


class TestMD5(unittest.TestCase):
    def setUp(self):
        # Store original implementation name
        self.original_implementation = sys.implementation.name
        # Clear the module from sys.modules to force reload
        if 'notecard.md5' in sys.modules:
            del sys.modules['notecard.md5']

    def tearDown(self):
        # Restore original implementation
        sys.implementation.name = self.original_implementation
        # Clear the module again
        if 'notecard.md5' in sys.modules:
            del sys.modules['notecard.md5']

    def test_non_cpython_implementation(self):
        """Test our custom MD5 implementation used in non-CPython environments"""
        # Set implementation to non-cpython before importing
        sys.implementation.name = 'non-cpython'
        import notecard.md5

        test_cases = [
            (b'', 'd41d8cd98f00b204e9800998ecf8427e'),
            (b'hello', '5d41402abc4b2a76b9719d911017c592'),
            (b'hello world', '5eb63bbbe01eeed093cb22bb8f5acdc3'),
            (b'The quick brown fox jumps over the lazy dog',
             '9e107d9d372bb6826bd81d3542a419d6'),
            (b'123456789', '25f9e794323b453885f5181f1b624d0b'),
            (b'!@#$%^&*()', '05b28d17a7b6e7024b6e5d8cc43a8bf7')
        ]

        for input_bytes, expected in test_cases:
            with self.subTest(input_bytes=input_bytes):
                result = notecard.md5.digest(input_bytes)
                self.assertEqual(result, expected)
