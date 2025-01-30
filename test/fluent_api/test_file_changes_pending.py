"""Tests for file.changes.pending functionality."""
from notecard import file


def test_file_changes_pending_basic(run_fluent_api_notecard_api_mapping_test):
    """Test basic file.changes.pending call."""
    run_fluent_api_notecard_api_mapping_test(
        file.pendingChanges, 'file.changes.pending', {})


def test_file_changes_pending_response(card):
    """Test file.changes.pending response structure."""
    card.Transaction.return_value = {
        'total': 42,
        'changes': 5
    }
    response = file.pendingChanges(card)
    assert 'total' in response
    assert isinstance(response['total'], int)
    assert 'changes' in response
    assert isinstance(response['changes'], int)


def test_file_changes_pending_error(card):
    """Test file.changes.pending error response."""
    card.Transaction.return_value = {"err": "Permission denied"}
    response = file.pendingChanges(card)
    assert "err" in response
    assert "Permission denied" in response["err"]


def test_file_changes_pending_malformed_response(card):
    """Test handling of malformed response data."""
    card.Transaction.return_value = {
        'total': "not-an-integer",
        'changes': None
    }
    response = file.pendingChanges(card)
    assert "err" in response
    assert "malformed response" in response["err"].lower()


def test_file_changes_pending_missing_fields(card):
    """Test handling of response missing required fields."""
    card.Transaction.return_value = {'total': 42}  # Missing changes field
    response = file.pendingChanges(card)
    assert "err" in response
    assert "missing required fields" in response["err"].lower()


def test_file_changes_pending_unexpected_fields(card):
    """Test handling of response with unexpected extra fields."""
    card.Transaction.return_value = {
        'total': 42,
        'changes': 5,
        'unexpected': 'field'
    }
    response = file.pendingChanges(card)
    # Should still succeed with expected fields present
    assert isinstance(response['total'], int)
    assert isinstance(response['changes'], int)


def test_file_changes_pending_zero_values(card):
    """Test handling of valid zero values in response."""
    card.Transaction.return_value = {
        'total': 0,
        'changes': 0
    }
    response = file.pendingChanges(card)
    assert response['total'] == 0
    assert response['changes'] == 0
