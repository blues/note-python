import unittest
import sys
from unittest.mock import MagicMock, patch
from notecard import Notecard
from notecard.validators import validate_card_object


class TestValidators(unittest.TestCase):

    def setUp(self):
        self.mock_notecard = MagicMock(spec=Notecard)
        # Store original implementation name
        self.original_implementation = sys.implementation.name
        # Clear the module from sys.modules to force reload
        if 'notecard.validators' in sys.modules:
            del sys.modules['notecard.validators']

    def tearDown(self):
        # Restore original implementation
        sys.implementation.name = self.original_implementation
        # Clear the module again
        if 'notecard.validators' in sys.modules:
            del sys.modules['notecard.validators']

    def test_validate_card_object_with_valid_notecard(self):
        @validate_card_object
        def test_func(card):
            return True

        result = test_func(self.mock_notecard)
        self.assertTrue(result)

    def test_validate_card_object_with_invalid_notecard(self):
        @validate_card_object
        def test_func(card):
            return True

        with self.assertRaises(Exception) as context:
            test_func("not a notecard")
        self.assertEqual(str(context.exception), "Notecard object required")

    @unittest.skipIf(sys.implementation.name != "cpython", "Function metadata only preserved in CPython")
    def test_validate_card_object_preserves_metadata(self):
        @validate_card_object
        def test_func(card):
            """Test function docstring."""
            return True

        self.assertEqual(test_func.__name__, "test_func")
        self.assertEqual(test_func.__doc__, "Test function docstring.")

    def test_validate_card_object_non_cpython(self):
        sys.implementation.name = 'non-cpython'
        from notecard.validators import validate_card_object

        @validate_card_object
        def test_func(card):
            return True

        result = test_func(self.mock_notecard)
        self.assertTrue(result)

    def test_validate_card_object_non_cpython_with_invalid_notecard(self):
        sys.implementation.name = 'non-cpython'
        from notecard.validators import validate_card_object

        @validate_card_object
        def test_func(card):
            return True

        with self.assertRaises(Exception) as context:
            test_func("not a notecard")
        self.assertEqual(str(context.exception), "Notecard object required")
