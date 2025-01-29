"""Test NTN support in hub module."""
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
