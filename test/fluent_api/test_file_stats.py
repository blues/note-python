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
    # Validate types only when fields are present
    if 'total' in response:
        assert isinstance(response['total'], int)
    if 'changes' in response:
        assert isinstance(response['changes'], int)
    if 'sync' in response:
        assert isinstance(response['sync'], bool)


def test_file_stats_with_error(card):
    """Test file.stats error handling."""
    card.Transaction.return_value = {"err": "File not found"}
    response = file.stats(card, file="nonexistent.qo")
    assert "err" in response
    assert "File not found" in response["err"]
