"""Tests for file.changes functionality."""
import pytest
from notecard import file


def test_file_changes_basic(run_fluent_api_notecard_api_mapping_test):
    """Test file.changes with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.changes, 'file.changes', {})


def test_file_changes_with_tracker(run_fluent_api_notecard_api_mapping_test):
    """Test file.changes with tracker parameter."""
    run_fluent_api_notecard_api_mapping_test(
        file.changes, 'file.changes', {'tracker': 'my_tracker'})


def test_file_changes_with_files(run_fluent_api_notecard_api_mapping_test):
    """Test file.changes with files parameter."""
    run_fluent_api_notecard_api_mapping_test(
        file.changes, 'file.changes', {'files': ['file1.qo', 'file2.qo']})


def test_file_changes_with_all_params(run_fluent_api_notecard_api_mapping_test):
    """Test file.changes with all parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.changes, 'file.changes', {
            'tracker': 'my_tracker',
            'files': ['file1.qo', 'file2.qo']
        })


def test_file_changes_response(card):
    """Test file.changes response structure."""
    card.Transaction.return_value = {
        'changes': 5,
        'total': 42,
        'info': {
            'file1.qo': {'changes': 2, 'total': 20},
            'file2.qo': {'changes': 3, 'total': 22}
        }
    }
    response = file.changes(card)
    assert 'changes' in response
    assert isinstance(response['changes'], int)
    assert 'total' in response
    assert isinstance(response['total'], int)
    assert 'info' in response
    assert isinstance(response['info'], dict)
    for file_info in response['info'].values():
        assert 'changes' in file_info
        assert isinstance(file_info['changes'], int)
        assert 'total' in file_info
        assert isinstance(file_info['total'], int)
