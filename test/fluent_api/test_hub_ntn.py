"""Test NTN support in hub module."""
import json
from unittest.mock import ANY, call
from notecard import hub


def test_sync_with_ntn(run_fluent_api_notecard_api_mapping_test):
    """Test hub.sync with NTN support."""
    run_fluent_api_notecard_api_mapping_test(
        hub.sync,
        "hub.sync",
        {"allow": True}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.sync,
        "hub.sync",
        {"allow": False}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.sync,
        "hub.sync",
        {"out": True}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.sync,
        "hub.sync",
        {"in_": True},
        {"in_": "in"}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.sync,
        "hub.sync",
        {"out": True, "in_": True},
        {"in_": "in"}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.sync,
        "hub.sync",
        {}
    )


def test_sync_boolean_serialization(card):
    """Test that boolean values are properly serialized in hub.sync."""
    hub.sync(card, in_=True, out=False, allow=True)
    # Verify the Transaction was called with correct boolean values
    expected_req = {
        'req': 'hub.sync',
        'in': True,
        'out': False,
        'allow': True
    }
    card.Transaction.assert_called_once_with(expected_req)
    # Verify JSON serialization format
    args = card.Transaction.call_args
    req_dict = args[0][0]
    # Verify boolean values are preserved after JSON serialization
    json_dict = json.loads(json.dumps(req_dict))
    assert json_dict["in"] is True
    assert json_dict["out"] is False
    assert json_dict["allow"] is True


def test_sync_status(run_fluent_api_notecard_api_mapping_test):
    """Test hub.syncStatus."""
    run_fluent_api_notecard_api_mapping_test(
        hub.syncStatus,
        "hub.sync.status",
        {"sync": True}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.syncStatus,
        "hub.sync.status",
        {}
    )


def test_status(run_fluent_api_notecard_api_mapping_test):
    """Test hub.status."""
    run_fluent_api_notecard_api_mapping_test(
        hub.status,
        "hub.status",
        {}
    )
