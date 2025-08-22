import pytest
from notecard import ntn


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            ntn.gps,
            'ntn.gps',
            {'on': True}
        ),
        (
            ntn.gps,
            'ntn.gps',
            {'off': True}
        ),
        (
            ntn.reset,
            'ntn.reset',
            {}
        ),
        (
            ntn.status,
            'ntn.status',
            {}
        )
    ]
)
class TestNtn:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
