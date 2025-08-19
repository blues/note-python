import pytest
from notecard import dfu


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            dfu.get,
            'dfu.get',
            {}
        ),
        (
            dfu.get,
            'dfu.get',
            {'length': 1024}
        ),
        (
            dfu.get,
            'dfu.get',
            {'length': 1024, 'offset': 512}
        ),
        (
            dfu.status,
            'dfu.status',
            {}
        ),
        (
            dfu.status,
            'dfu.status',
            {'name': 'firmware.bin'}
        ),
        (
            dfu.status,
            'dfu.status',
            {'stop': True, 'on': True}
        ),
        (
            dfu.status,
            'dfu.status',
            {'status': 'ready', 'version': '1.0.0', 'vvalue': 100}
        ),
        (
            dfu.status,
            'dfu.status',
            {'err': 'error message'}
        ),
        (
            dfu.status,
            'dfu.status',
            {'off': True}
        )
    ]
)
class TestDfu:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
