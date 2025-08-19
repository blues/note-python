import pytest
from notecard import var


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            var.delete,
            'var.delete',
            {'name': 'my_var'}
        ),
        (
            var.delete,
            'var.delete',
            {'name': 'my_var', 'file': 'config.db'}
        ),
        (
            var.get,
            'var.get',
            {'name': 'my_var'}
        ),
        (
            var.get,
            'var.get',
            {'name': 'my_var', 'file': 'config.db'}
        ),
        (
            var.set,
            'var.set',
            {'name': 'my_var', 'text': 'my_value'}
        ),
        (
            var.set,
            'var.set',
            {'name': 'my_var', 'value': 42, 'file': 'config.db'}
        ),
        (
            var.set,
            'var.set',
            {'name': 'my_var', 'flag': True, 'sync': True}
        )
    ]
)
class TestVar:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
