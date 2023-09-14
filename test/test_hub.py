import pytest
from notecard import hub


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            hub.get,
            'hub.get',
            {}
        ),
        (
            hub.log,
            'hub.log',
            {
                'text': 'com.blues.tester',
                'alert': True,
                'sync': True
            }
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
            }
        ),
        (
            hub.status,
            'hub.status',
            {}
        ),
        (
            hub.sync,
            'hub.sync',
            {}
        ),
        (
            hub.syncStatus,
            'hub.sync.status',
            {'sync': True}
        )
    ]
)
class TestHub:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
