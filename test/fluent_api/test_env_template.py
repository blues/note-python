"""Tests for env.template functionality."""
from notecard import env


def test_env_template_basic(run_fluent_api_notecard_api_mapping_test):
    """Test env.template with no body parameter."""
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {})


def test_env_template_with_boolean(run_fluent_api_notecard_api_mapping_test):
    """Test env.template with boolean type hint."""
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': {'my_bool': True}})


def test_env_template_with_string_pre_321(
        run_fluent_api_notecard_api_mapping_test):
    """Test string type hint in env.template.

    For pre v3.2.1 format."""
    body = {'my_string': '42'}
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': body})


def test_env_template_with_string_post_321(
        run_fluent_api_notecard_api_mapping_test):
    """Test string type hint in env.template.

    For post v3.2.1 format."""
    body = {'my_string': 'variable'}
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': body})


def test_env_template_with_signed_integers(
        run_fluent_api_notecard_api_mapping_test):
    """Test signed integer hints.

    Covers all supported sizes."""
    body = {
        'int8': 11,    # 1 byte signed
        'int16': 12,   # 2 byte signed
        'int24': 13,   # 3 byte signed
        'int32': 14,   # 4 byte signed
        'int64': 18    # 8 byte signed
    }
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': body})


def test_env_template_with_unsigned_integers(
        run_fluent_api_notecard_api_mapping_test):
    """Test unsigned integer hints.

    Covers all supported sizes."""
    body = {
        'uint8': 21,   # 1 byte unsigned
        'uint16': 22,  # 2 byte unsigned
        'uint24': 23,  # 3 byte unsigned
        'uint32': 24   # 4 byte unsigned
    }
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': body})


def test_env_template_with_floats(run_fluent_api_notecard_api_mapping_test):
    """Test env.template with float type hints."""
    body = {
        'float16': 12.1,  # 2 byte float
        'float32': 14.1,  # 4 byte float
        'float64': 18.1   # 8 byte float
    }
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': body})


def test_env_template_with_mixed_types(
        run_fluent_api_notecard_api_mapping_test):
    """Test mixed type hints.

    Tests bool, str, float, int."""
    body = {
        'active': True,
        'name': '32',
        'temperature': 14.1,
        'counter': 12
    }
    run_fluent_api_notecard_api_mapping_test(
        env.template, 'env.template', {'body': body})


def test_env_template_response(card):
    """Test env.template response contains bytes field."""
    card.Transaction.return_value = {'bytes': 42}
    response = env.template(card)
    assert 'bytes' in response
    assert isinstance(response['bytes'], int)
