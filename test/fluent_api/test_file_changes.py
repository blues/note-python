"""Tests for file.changes functionality."""
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


def test_file_changes_with_all_params(
        run_fluent_api_notecard_api_mapping_test):
    """Test file.changes with all parameters."""
    params = {'tracker': 'my_tracker', 'files': ['file1.qo', 'file2.qo']}
    run_fluent_api_notecard_api_mapping_test(
        file.changes, 'file.changes', params)


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
    # First validate the response has all required fields
    assert 'changes' in response
    assert 'total' in response
    assert 'info' in response
    # Then validate the types
    assert isinstance(response['changes'], int)
    assert isinstance(response['total'], int)
    assert isinstance(response['info'], dict)
    # Only if info is a dict, validate its contents
    if isinstance(response['info'], dict):
        for filename, file_info in response['info'].items():
            assert isinstance(file_info, dict)
            assert 'changes' in file_info
            assert 'total' in file_info
            assert isinstance(file_info['changes'], int)
            assert isinstance(file_info['total'], int)


def test_file_changes_with_invalid_tracker(card):
    """Test file.changes with invalid tracker format."""
    card.Transaction.return_value = {"err": "Invalid tracker format"}
    response = file.changes(card, tracker="@@@!!!")
    assert "err" in response
    assert "Invalid tracker format" in response["err"]


def test_file_changes_with_malformed_response(card):
    """Test handling of malformed response data."""
    card.Transaction.return_value = {
        "changes": "not-an-integer",
        "total": None,
        "info": "should-be-object"
    }
    response = file.changes(card)
    assert "err" in response
    assert "malformed response" in response["err"].lower()


def test_file_changes_with_missing_info(card):
    """Test handling of response missing required fields."""
    card.Transaction.return_value = {"changes": 5}  # Missing total and info
    response = file.changes(card)
    assert "err" in response
    assert "missing required fields" in response["err"].lower()


def test_file_changes_with_nonexistent_files(card):
    """Test file.changes with non-existent files."""
    card.Transaction.return_value = {"err": "File not found"}
    response = file.changes(card, files=["nonexistent.qo"])
    assert "err" in response
    assert "File not found" in response["err"]
