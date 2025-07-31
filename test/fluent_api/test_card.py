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
            card.wireless,
            'card.wireless',
            {
                'mode': 'auto',
                'apn': 'myapn.nb'
            }
        ),
        (
            card.transport,
            'card.transport',
            {
                'method': 'wifi-cell-ntn',
                'allow': True
            }
        ),
        (
            card.power,
            'card.power',
            {
                'minutes': 10,
                'reset': True
            }
        ),
        (
            card.location,
            'card.location',
            {}
        ),
        (
            card.locationMode,
            'card.location.mode',
            {
                'mode': 'periodic',
                'seconds': 300,
                'vseconds': 'high',
                'lat': 42.5776,
                'lon': -70.87134,
                'max': 60
            }
        ),
        (
            card.locationTrack,
            'card.location.track',
            {
                'start': True,
                'heartbeat': True,
                'hours': 2,
                'sync': True,
                'stop': False,
                'file': 'location.qo'
            }
        ),
        (
            card.binary,
            'card.binary',
            {
                'delete': True
            }
        ),
        (
            card.binaryGet,
            'card.binary.get',
            {
                'cobs': 1024,
                'offset': 0,
                'length': 512
            }
        ),
        (
            card.binaryPut,
            'card.binary.put',
            {
                'offset': 0,
                'cobs': 1024,
                'status': 'd41d8cd98f00b204e9800998ecf8427e'
            }
        ),
        (
            card.carrier,
            'card.carrier',
            {
                'mode': 'charging'
            }
        ),
        (
            card.contact,
            'card.contact',
            {
                'name': 'Tom Turkey',
                'org': 'Blues',
                'role': 'Head of Security',
                'email': 'tom@blues.com'
            }
        ),
        (
            card.aux,
            'card.aux',
            {
                'mode': 'gpio',
                'usage': ['input', 'output', 'count'],
                'seconds': 60,
                'max': 10,
                'start': True,
                'gps': False,
                'rate': 115200,
                'sync': True,
                'file': 'aux.qo',
                'connected': False,
                'limit': True,
                'sensitivity': 50,
                'ms': 100,
                'count': 5,
                'offset': 1
            }
        ),
        (
            card.auxSerial,
            'card.aux.serial',
            {
                'mode': 'notify,accel',
                'duration': 30,
                'rate': 9600,
                'limit': True,
                'max': 1024,
                'ms': 500,
                'minutes': 5
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
