"""Tests for note.template with array support."""
from notecard import note


def test_template_with_array_body(run_fluent_api_notecard_api_mapping_test):
    """Test note.template with an array body."""
    run_fluent_api_notecard_api_mapping_test(
        note.template, 'note.template',
        {'body': ['item1', 'item2', 'item3']})


def test_template_with_array_in_body(run_fluent_api_notecard_api_mapping_test):
    """Test note.template with an object containing an array."""
    run_fluent_api_notecard_api_mapping_test(
        note.template, 'note.template',
        {'body': {'list_field': ['item1', 'item2']}})


def test_template_with_nested_arrays(run_fluent_api_notecard_api_mapping_test):
    """Test note.template with nested arrays in body."""
    run_fluent_api_notecard_api_mapping_test(
        note.template, 'note.template',
        {'body': {'matrix': [[1, 2], [3, 4]]}})


def test_template_with_mixed_types(run_fluent_api_notecard_api_mapping_test):
    """Test note.template with mixed types in arrays."""
    run_fluent_api_notecard_api_mapping_test(
        note.template, 'note.template',
        {'body': {'mixed': [1, "text", True, 3.14]}})


def test_template_response_with_array(card):
    """Test note.template response handling with array data."""
    card.Transaction.return_value = {
        'body': ['response_item1', 'response_item2']
    }
    response = note.template(card, body=['test1', 'test2'])
    assert isinstance(response, dict)
    if 'body' in response:
        assert isinstance(response['body'], list)
