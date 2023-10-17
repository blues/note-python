import pytest
from notecard import env


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            env.default,
            'env.default',
            {'name': 'my_var', 'text': 'my_text'}
        ),
        (
            env.get,
            'env.get',
            {'name': 'my_var'}
        ),
        (
            env.modified,
            'env.modified',
            {}
        ),
        (
            env.set,
            'env.set',
            {'name': 'my_var', 'text': 'my_text'}
        )
    ]
)
class TestEnv:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
