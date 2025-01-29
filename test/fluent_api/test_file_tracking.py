"""Tests for file tracking and monitoring functionality."""
from notecard import file


def test_file_monitor_basic(run_fluent_api_notecard_api_mapping_test):
    """Test basic file monitoring without options."""
    run_fluent_api_notecard_api_mapping_test(
        file.monitor,
        'file.monitor',
        {}
    )


def test_file_monitor_with_files(run_fluent_api_notecard_api_mapping_test):
    """Test monitoring specific files."""
    run_fluent_api_notecard_api_mapping_test(
        file.monitor,
        'file.monitor',
        {'files': ['data.qo', 'settings.db']}
    )


def test_file_monitor_with_files_list(run_fluent_api_notecard_api_mapping_test):
    """Test monitoring with multiple files."""
    run_fluent_api_notecard_api_mapping_test(
        file.monitor,
        'file.monitor',
        {'files': ['data.qo', 'settings.db']}
    )


def test_file_track_with_invalid_interval(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with invalid interval value."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'interval': -1}
    )


def test_file_track_with_invalid_duration(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with invalid duration value."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'duration': -1}
    )


def test_file_monitor_with_files_and_detail_level(run_fluent_api_notecard_api_mapping_test):
    """Test monitoring with files list."""
    run_fluent_api_notecard_api_mapping_test(
        file.monitor,
        'file.monitor',
        {
            'files': ['data.qo', 'settings.db']
        }
    )


def test_file_monitor_with_all_params(run_fluent_api_notecard_api_mapping_test):
    """Test monitoring with all available parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.monitor,
        'file.monitor',
        {
            'files': ['data.qo', 'settings.db']
        }
    )


def test_file_stats_with_no_params(run_fluent_api_notecard_api_mapping_test):
    """Test file stats with no parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.stats,
        'file.stats',
        {}
    )


def test_file_track_with_zero_duration(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with zero duration (should be valid)."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'duration': 0}
    )


def test_file_track_with_zero_interval(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with zero interval (should be valid)."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'interval': 0}
    )


def test_file_monitor_with_empty_files(run_fluent_api_notecard_api_mapping_test):
    """Test monitoring with empty files list."""
    run_fluent_api_notecard_api_mapping_test(
        file.monitor,
        'file.monitor',
        {'files': []}
    )


def test_file_track_basic(run_fluent_api_notecard_api_mapping_test):
    """Test basic file tracking without options."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {}
    )


def test_file_track_with_files(run_fluent_api_notecard_api_mapping_test):
    """Test tracking specific files."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'files': ['data.qo', 'config.db']}
    )


def test_file_track_with_interval(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with custom interval."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'interval': 60}
    )


def test_file_track_with_duration(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with specified duration."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {'duration': 3600}
    )


def test_file_track_full_config(run_fluent_api_notecard_api_mapping_test):
    """Test tracking with all parameters."""
    run_fluent_api_notecard_api_mapping_test(
        file.track,
        'file.track',
        {
            'files': ['data.qo'],
            'interval': 30,
            'duration': 1800
        }
    )


def test_file_stats_basic(run_fluent_api_notecard_api_mapping_test):
    """Test basic file stats without extended info."""
    run_fluent_api_notecard_api_mapping_test(
        file.stats,
        'file.stats',
        {}
    )


def test_file_stats_with_file(run_fluent_api_notecard_api_mapping_test):
    """Test file stats with specific file parameter."""
    run_fluent_api_notecard_api_mapping_test(
        file.stats,
        'file.stats',
        {'file': 'data.qo'}
    )
