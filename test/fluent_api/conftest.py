import sys
import os
import pytest
from unittest.mock import MagicMock

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import notecard  # noqa: E402


@pytest.fixture
def run_fluent_api_notecard_api_mapping_test():
    def _run_test(fluent_api, notecard_api_name, req_params, rename_key_map=None, rename_value_map=None):
        card = notecard.Notecard()
        card.Transaction = MagicMock()

        fluent_api(card, **req_params)
        expected_notecard_api_req = {'req': notecard_api_name, **req_params}

        # There are certain fluent APIs that have keyword arguments that don't
        # map exactly onto the Notecard API. For example, note.changes takes a
        # 'maximum' parameter, but in the JSON request that gets sent to the
        # Notecard, it's sent as 'max'. The rename_key_map allows a test to specify
        # how a fluent API's keyword args map to Notecard API args, in cases
        # where they differ.
        if rename_key_map is not None:
            for old_key, new_key in rename_key_map.items():
                expected_notecard_api_req[new_key] = expected_notecard_api_req.pop(old_key)

        # Additionally, some Notecard API args have values that are not directly
        # mapped, but are instead derived from the value of another arg. For
        # example, note.template takes a 'compact' parameter, but the value of
        # that parameter is actually derived from the value of the 'format'
        # parameter. The rename_value_map allows a test to specify how a fluent
        # API's keyword args map to Notecard API args, in cases where the value
        # of one arg is derived from the value of another arg.
        if rename_value_map is not None:
            for key, new_value in rename_value_map.items():
                expected_notecard_api_req[key] = new_value

        card.Transaction.assert_called_once_with(expected_notecard_api_req)

    return _run_test


@pytest.fixture
def run_fluent_api_invalid_notecard_test():
    def _run_test(fluent_api, req_params, rename_key_map=None, rename_value_map=None):
        with pytest.raises(Exception, match='Notecard object required'):
            # Call with None instead of a valid Notecard object.
            fluent_api(None, **req_params)

    return _run_test
