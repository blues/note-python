"""Tests for file.changes.pending functionality."""
from notecard import file


def test_file_changes_pending_basic(run_fluent_api_notecard_api_mapping_test):
    """Test file.changes.pending with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.pendingChanges, 'file.changes.pending', {})


def test_file_changes_pending_response(card):
    """Test file.changes.pending response structure."""
    card.Transaction.return_value = {
        'total': 42,
        'changes': 5
    }
    response = file.pendingChanges(card)
    # Validate types only when fields are present
    if 'total' in response:
        assert isinstance(response['total'], int)
    if 'changes' in response:
        assert isinstance(response['changes'], int)


def test_file_changes_pending_with_error(card):
    """Test file.changes.pending error handling."""
    card.Transaction.return_value = {"err": "Internal error"}
    response = file.pendingChanges(card)
    assert "err" in response
    assert "Internal error" in response["err"]
