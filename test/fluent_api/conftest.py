import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import notecard  # noqa: E402


class MockNotecard(notecard.Notecard):
    def Reset(self):
        pass

    def lock(self):
        pass

    def unlock(self):
        pass

    def _transact(self, req_bytes, rsp_expected, timeout_secs):
        pass


@pytest.fixture
def card():
    """Create a mock Notecard instance for testing."""
    card = MockNotecard()
    card.Transaction = MagicMock()
    return card


@pytest.fixture
def run_fluent_api_notecard_api_mapping_test():
    def _run_test(fluent_api, notecard_api_name, req_params, rename_map=None):
        card = MockNotecard()
        card.Transaction = MagicMock()
        fluent_api(card)
        expected_req = {"req": notecard_api_name}
        expected_req.update(req_params)
        if rename_map:
            for old_key, new_key in rename_map.items():
                if old_key in expected_req:
                    expected_req[new_key] = expected_req.pop(old_key)
        card.Transaction.assert_called_once_with(expected_req)
    return _run_test


@pytest.fixture
def run_fluent_api_invalid_notecard_test():
    def _run_test(fluent_api, req_params):
        with pytest.raises(Exception, match='Notecard object required'):
            # Call with None instead of a valid Notecard object.
            fluent_api(None, **req_params)

    return _run_test
