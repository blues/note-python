import pytest
from notecard import hub


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params,rename_key_map',
    [
        (
            hub.get,
            'hub.get',
            {},
            None
        ),
        (
            hub.log,
            'hub.log',
            {
                'text': 'com.blues.tester',
                'alert': True,
                'sync': True
            },
            None
        ),
        (
            hub.set,
            'hub.set',
            {
                'product': 'com.blues.tester',
                'sn': 'foo',
                'mode': 'continuous',
                'outbound': 2,
                'inbound': 60,
                'duration': 5,
                'sync': True,
                'align': True,
                'voutbound': '2.3',
                'vinbound': '3.3',
                'host': 'http://hub.blues.foo'
            },
            None
        ),
        (
            hub.status,
            'hub.status',
            {},
            None
        ),
        (
            hub.sync,
            'hub.sync',
            {},
            None
        ),
        (
            hub.syncStatus,
            'hub.sync.status',
            {'sync': True},
            None
        ),
        (
            hub.signal,
            'hub.signal',
            {'seconds': 30},
            None
        ),
        (
            hub.set,
            'hub.set',
            {
                'details': 'LoRaWAN details',
                'off': True,
                'on': False,
                'seconds': 300,
                'umin': True,
                'uoff': False,
                'uperiodic': True,
                'version': '1.0.0'
            },
            None
        ),
        (
            hub.sync,
            'hub.sync',
            {
                'allow': True,
                'in_': False,
                'out_': True
            },
            {
                'in_': 'in',
                'out_': 'out'
            }
        )
    ]
)
class TestHub:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params, rename_key_map,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params, rename_key_map)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params, rename_key_map,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params, rename_key_map)
