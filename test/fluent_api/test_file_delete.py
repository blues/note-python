"""Tests for file.delete functionality."""
from notecard import file


def test_file_delete_basic(run_fluent_api_notecard_api_mapping_test):
    """Test file.delete with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.delete, 'file.delete', {})


def test_file_delete_with_files(run_fluent_api_notecard_api_mapping_test):
    """Test file.delete with files parameter."""
    run_fluent_api_notecard_api_mapping_test(
        file.delete, 'file.delete', {'files': ['file1.qo', 'file2.qo']})


def test_file_delete_response(card):
    """Test file.delete response structure."""
    card.Transaction.return_value = {}
    response = file.delete(card, files=['file1.qo'])
    assert isinstance(response, dict)
    assert card.Transaction.call_args[0][0] == {
        'req': 'file.delete',
        'files': ['file1.qo']
    }


def test_file_delete_nonexistent_files(card):
    """Test file.delete with non-existent files."""
    card.Transaction.return_value = {"err": "File not found"}
    response = file.delete(card, files=["nonexistent.qo"])
    assert "err" in response
    assert "File not found" in response["err"]


def test_file_delete_mixed_existence(card):
    """Test file.delete with mix of existing and non-existent files."""
    card.Transaction.return_value = {"err": "Some files not found"}
    response = file.delete(card, files=["existing.qo", "nonexistent.qo"])
    assert "err" in response
    assert "not found" in response["err"].lower()


def test_file_delete_invalid_filename(card):
    """Test file.delete with invalid filename format."""
    card.Transaction.return_value = {"err": "Invalid filename format"}
    response = file.delete(card, files=["invalid/path.qo"])
    assert "err" in response
    assert "Invalid filename" in response["err"]
