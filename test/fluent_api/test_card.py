import pytest
from notecard import card


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            card.attn,
            'card.attn',
            {
                'mode': 'arm',
                'files': ['data.qi', 'my-settings.db'],
                'seconds': 60,
                'payload': 'ewogICJpbnRlcnZhbHMiOiI2MCwxMiwxNCIKfQ==',
                'start': True
            }
        ),
        (
            card.status,
            'card.status',
            {}
        ),
        (
            card.time,
            'card.time',
            {}
        ),
        (
            card.temp,
            'card.temp',
            {'minutes': 5}
        ),
        (
            card.version,
            'card.version',
            {}
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'hours': 1,
                'offset': 2,
                'vmax': 1.1,
                'vmin': 1.2
            }
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'usb': True
            }
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'alert': True
            }
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'usb': True,
                'alert': True
            }
        ),
        (
            card.wireless,
            'card.wireless',
            {
                'mode': 'auto',
                'apn': 'myapn.nb'
            }
        )
    ]
)
class TestCard:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
