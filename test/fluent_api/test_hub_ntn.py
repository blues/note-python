"""Test NTN support in hub module."""
import pytest

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
        {}
    )


def test_sync_status_with_ntn(run_fluent_api_notecard_api_mapping_test):
    """Test hub.syncStatus with NTN support."""
    run_fluent_api_notecard_api_mapping_test(
        hub.syncStatus,
        "hub.sync.status",
        {"ntn": True}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.syncStatus,
        "hub.sync.status",
        {"sync": True, "ntn": True}
    )



def test_status_with_ntn(run_fluent_api_notecard_api_mapping_test):
    """Test hub.status with NTN support."""
    run_fluent_api_notecard_api_mapping_test(
        hub.status,
        "hub.status",
        {"ntn": True}
    )

    run_fluent_api_notecard_api_mapping_test(
        hub.status,
        "hub.status",
        {}
    )
