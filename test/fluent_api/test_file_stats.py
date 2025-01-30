"""Tests for file.stats functionality."""
from notecard import file


def test_file_stats_basic(run_fluent_api_notecard_api_mapping_test):
    """Test file.stats with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.stats, 'file.stats', {})


def test_file_stats_with_file(run_fluent_api_notecard_api_mapping_test):
    """Test file.stats with file parameter."""
    run_fluent_api_notecard_api_mapping_test(
        file.stats, 'file.stats', {'file': 'test.qo'})


def test_file_stats_response(card):
    """Test file.stats response structure."""
    card.Transaction.return_value = {
        'total': 42,
        'changes': 5,
        'sync': True
    }
    response = file.stats(card)
    assert 'total' in response
    assert isinstance(response['total'], int)
    assert 'changes' in response
    assert isinstance(response['changes'], int)
    assert 'sync' in response
    assert isinstance(response['sync'], bool)


def test_file_stats_specific_file_response(card):
    """Test file.stats response for specific file."""
    test_file = 'sensors.qo'
    card.Transaction.return_value = {
        'total': 10,
        'changes': 2,
        'sync': False
    }
    response = file.stats(card, file=test_file)
    assert 'total' in response
    assert isinstance(response['total'], int)
    assert 'changes' in response
    assert isinstance(response['changes'], int)
    assert 'sync' in response
    assert isinstance(response['sync'], bool)
    # Verify request structure
    assert card.Transaction.call_args[0][0] == {
        'req': 'file.stats',
        'file': test_file
    }


def test_file_stats_invalid_filename(card):
    """Test file.stats with invalid filename format."""
    card.Transaction.return_value = {"err": "Invalid file name"}
    response = file.stats(card, file=":BADFILE:?")
    assert "err" in response
    assert "Invalid file name" in response["err"]


def test_file_stats_nonexistent_file(card):
    """Test file.stats with non-existent file."""
    card.Transaction.return_value = {"err": "File not found"}
    response = file.stats(card, file="nonexistent.qo")
    assert "err" in response
    assert "File not found" in response["err"]


def test_file_stats_malformed_response(card):
    """Test handling of malformed response data."""
    card.Transaction.return_value = {
        'total': "not-an-integer",
        'changes': None,
        'sync': "not-a-boolean"
    }
    response = file.stats(card)
    assert "err" in response
    assert "malformed response" in response["err"].lower()


def test_file_stats_missing_fields(card):
    """Test handling of response missing required fields."""
    card.Transaction.return_value = {
        'total': 42  # Missing changes and sync
    }
    response = file.stats(card)
    assert "err" in response
    assert "missing required fields" in response["err"].lower()


def test_file_stats_unexpected_fields(card):
    """Test handling of response with unexpected extra fields."""
    card.Transaction.return_value = {
        'total': 42,
        'changes': 5,
        'sync': True,
        'unexpected': 'field'
    }
    response = file.stats(card)
    # Should still succeed with expected fields present
    assert isinstance(response['total'], int)
    assert isinstance(response['changes'], int)
    assert isinstance(response['sync'], bool)


def test_file_stats_zero_values(card):
    """Test handling of valid zero values in response."""
    card.Transaction.return_value = {
        'total': 0,
        'changes': 0,
        'sync': False
    }
    response = file.stats(card)
    assert response['total'] == 0
    assert response['changes'] == 0
    assert response['sync'] is False
