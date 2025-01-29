"""Test power management features in card module."""
from notecard import card


def test_card_power_no_params(run_fluent_api_notecard_api_mapping_test):
    """Test power() with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        card.power,
        'card.power',
        {}
    )


def test_card_power_minutes(run_fluent_api_notecard_api_mapping_test):
    """Test power() with minutes parameter."""
    run_fluent_api_notecard_api_mapping_test(
        card.power,
        'card.power',
        {'minutes': 120}
    )


def test_card_power_reset(run_fluent_api_notecard_api_mapping_test):
    """Test power() with reset parameter."""
    run_fluent_api_notecard_api_mapping_test(
        card.power,
        'card.power',
        {'reset': True}
    )


def test_card_power_all_params(run_fluent_api_notecard_api_mapping_test):
    """Test power() with all parameters."""
    run_fluent_api_notecard_api_mapping_test(
        card.power,
        'card.power',
        {'minutes': 60, 'reset': True}
    )


def test_card_power_minutes_type(run_fluent_api_notecard_api_mapping_test):
    """Test that minutes parameter is properly handled as integer."""
    run_fluent_api_notecard_api_mapping_test(
        card.power,
        'card.power',
        {'minutes': 30}
    )


def test_card_power_reset_type(run_fluent_api_notecard_api_mapping_test):
    """Test that reset parameter is properly handled as boolean."""
    run_fluent_api_notecard_api_mapping_test(
        card.power,
        'card.power',
        {'reset': True}
    )


def test_voltage_usb_monitoring(run_fluent_api_notecard_api_mapping_test):
    """Test USB power state monitoring."""
    run_fluent_api_notecard_api_mapping_test(
        card.voltage,
        'card.voltage',
        {'usb': True}
    )


def test_voltage_alert_handling(run_fluent_api_notecard_api_mapping_test):
    """Test alert parameter handling."""
    run_fluent_api_notecard_api_mapping_test(
        card.voltage,
        'card.voltage',
        {'alert': True}
    )


def test_voltage_usb_with_alert(run_fluent_api_notecard_api_mapping_test):
    """Test combined USB monitoring and alert functionality."""
    run_fluent_api_notecard_api_mapping_test(
        card.voltage,
        'card.voltage',
        {'usb': True, 'alert': True}
    )


def test_voltage_with_all_parameters(run_fluent_api_notecard_api_mapping_test):
    """Test voltage with all available parameters."""
    run_fluent_api_notecard_api_mapping_test(
        card.voltage,
        'card.voltage',
        {
            'hours': 24,
            'offset': 1,
            'vmax': 5.0,
            'vmin': 3.3,
            'usb': True,
            'alert': True
        }
    )
