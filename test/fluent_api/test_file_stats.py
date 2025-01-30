"""Tests for file.stats functionality."""
import pytest
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
