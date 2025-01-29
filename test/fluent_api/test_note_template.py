"""Tests for note.template API."""


import pytest
from unittest.mock import MagicMock
from notecard import note


@pytest.fixture
def mock_card():
    card = MagicMock()
    card.Transaction.return_value = {"success": True}
    return card


def test_template_basic(mock_card):
    note.template(mock_card, file="test.qo")
    assert mock_card.Transaction.called
    assert mock_card.Transaction.call_args[0][0] == {
        "req": "note.template",
        "file": "test.qo"
    }


def test_template_with_valid_types(mock_card):
    body = {
        "bool_field": True,
        "int_field": 42,
        "float_field": 3.14,
        "string_field": "test"
    }
    note.template(mock_card, file="test.qo", body=body)
    assert mock_card.Transaction.called
    assert mock_card.Transaction.call_args[0][0]["body"] == body


def test_template_float_to_int_conversion(mock_card):
    body = {"whole_number": 42.0}
    note.template(mock_card, body=body)
    assert mock_card.Transaction.call_args[0][0]["body"]["whole_number"] == 42


def test_template_invalid_type(mock_card):
    body = {"invalid_field": {"nested": "object"}}
    result = note.template(mock_card, body=body)
    assert "err" in result
    assert "invalid_field" in result["err"]
    assert not mock_card.Transaction.called


def test_template_invalid_length(mock_card):
    result = note.template(mock_card, length=-1)
    assert "err" in result
    assert "Length" in result["err"]
    assert not mock_card.Transaction.called


def test_template_with_binary(mock_card):
    note.template(mock_card, length=32)
    assert mock_card.Transaction.called
    req = mock_card.Transaction.call_args[0][0]
    assert req["length"] == 32
    assert req["binary"] is True


def test_template_invalid_port(mock_card):
    result = note.template(mock_card, port=101)
    assert "err" in result
    assert "Port" in result["err"]
    assert not mock_card.Transaction.called


def test_template_compact_format(mock_card):
    note.template(mock_card, compact=True)
    assert mock_card.Transaction.called
    assert mock_card.Transaction.call_args[0][0]["format"] == "compact"


def test_template_compact_with_allowed_metadata(mock_card):
    body = {
        "field": "value",
        "_time": "2023-01-01",
        "_lat": 12.34,
        "_lon": 56.78,
        "_loc": "NYC"
    }
    note.template(mock_card, body=body, compact=True)
    assert mock_card.Transaction.called
    assert mock_card.Transaction.call_args[0][0]["body"] == body


def test_template_compact_with_invalid_metadata(mock_card):
    body = {
        "field": "value",
        "_invalid": "not allowed"
    }
    result = note.template(mock_card, body=body, compact=True)
    assert "err" in result
    assert "_invalid" in result["err"]
    assert not mock_card.Transaction.called


def test_template_full_configuration(mock_card):
    body = {
        "temperature": 21.5,
        "humidity": 45,
        "active": True,
        "location": "warehouse",
        "_time": "2023-01-01"
    }
    note.template(
        mock_card,
        file="sensors.qo",
        body=body,
        length=32,
        port=1,
        compact=True
    )
    assert mock_card.Transaction.called
    req = mock_card.Transaction.call_args[0][0]
    assert req["file"] == "sensors.qo"
    assert req["body"] == body
    assert req["length"] == 32
    assert req["binary"] is True
    assert req["port"] == 1
    assert req["format"] == "compact"
