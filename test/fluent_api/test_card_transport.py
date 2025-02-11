"""Tests for card.transport functionality."""
from notecard import card


def test_transport_basic(run_fluent_api_notecard_api_mapping_test):
    """Test card.transport with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        card.transport, 'card.transport', {})


def test_transport_method(run_fluent_api_notecard_api_mapping_test):
    """Test card.transport with method parameter."""
    run_fluent_api_notecard_api_mapping_test(
        card.transport, 'card.transport', {'method': 'ntn'})


def test_transport_allow(run_fluent_api_notecard_api_mapping_test):
    """Test card.transport with allow parameter."""
    run_fluent_api_notecard_api_mapping_test(
        card.transport, 'card.transport', {'allow': True})


def test_transport_all_params(run_fluent_api_notecard_api_mapping_test):
    """Test card.transport with all parameters."""
    run_fluent_api_notecard_api_mapping_test(
        card.transport, 'card.transport',
        {'method': 'wifi-cell-ntn', 'allow': True})


def test_transport_invalid_allow(card):
    """Test card.transport with invalid allow parameter."""
    result = card.transport(card, allow="not-a-boolean")
    assert "err" in result
    assert "allow parameter must be a boolean" in result["err"]


def test_transport_ntn_method(card):
    """Test card.transport with NTN method."""
    card.Transaction.return_value = {"connected": True}
    result = card.transport(card, method="ntn")
    assert card.Transaction.called
    assert card.Transaction.call_args[0][0] == {
        "req": "card.transport",
        "method": "ntn"
    }
    assert result == {"connected": True}


def test_transport_wifi_ntn_method(card):
    """Test card.transport with WiFi-NTN method."""
    card.Transaction.return_value = {"connected": True}
    result = card.transport(card, method="wifi-ntn")
    assert card.Transaction.called
    assert card.Transaction.call_args[0][0] == {
        "req": "card.transport",
        "method": "wifi-ntn"
    }
    assert result == {"connected": True}


def test_transport_cell_ntn_method(card):
    """Test card.transport with Cell-NTN method."""
    card.Transaction.return_value = {"connected": True}
    result = card.transport(card, method="cell-ntn")
    assert card.Transaction.called
    assert card.Transaction.call_args[0][0] == {
        "req": "card.transport",
        "method": "cell-ntn"
    }
    assert result == {"connected": True}


def test_transport_wifi_cell_ntn_method(card):
    """Test card.transport with WiFi-Cell-NTN method."""
    card.Transaction.return_value = {"connected": True}
    result = card.transport(card, method="wifi-cell-ntn")
    assert card.Transaction.called
    assert card.Transaction.call_args[0][0] == {
        "req": "card.transport",
        "method": "wifi-cell-ntn"
    }
    assert result == {"connected": True}
