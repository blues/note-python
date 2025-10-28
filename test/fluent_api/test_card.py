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
            card.attn,
            'card.attn',
            {
                'verify': True
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
            card.temp,
            'card.temp',
            {
                'status': 'usb:15;high:30;normal:60;720',
                'stop': True,
                'sync': True
            }
        ),
        (
            card.version,
            'card.version',
            {}
        ),
        (
            card.version,
            'card.version',
            {'api': True}
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
                'mode': 'charging',
                'name': 'voltage_sensor',
                'calibration': 1.1
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
            card.wireless,
            'card.wireless',
            {
                'method': 'dual-primary-secondary'
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
            card.transport,
            'card.transport',
            {
                'seconds': 300,
                'umin': True
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
            card.locationMode,
            'card.location.mode',
            {
                'minutes': 10,
                'threshold': 100
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
            card.locationTrack,
            'card.location.track',
            {
                'payload': 'ewogICJkYXRhIjogImV4YW1wbGUiCn0='
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
        ),
        (
            card.dfu,
            'card.dfu',
            {
                'name': 'esp32',
                'on': True,
                'off': False,
                'seconds': 300,
                'stop': True,
                'start': False,
                'mode': 'secure'
            }
        ),
        (
            card.illumination,
            'card.illumination',
            {}
        ),
        (
            card.io,
            'card.io',
            {
                'i2c': 24,
                'mode': '+busy'
            }
        ),
        (
            card.led,
            'card.led',
            {
                'mode': 'red',
                'on': True,
                'off': False
            }
        ),
        (
            card.monitor,
            'card.monitor',
            {
                'mode': 'green',
                'count': 5,
                'usb': True
            }
        ),
        (
            card.motion,
            'card.motion',
            {
                'minutes': 10
            }
        ),
        (
            card.motionMode,
            'card.motion.mode',
            {
                'start': True,
                'stop': False,
                'seconds': 30,
                'sensitivity': 0,
                'motion': 5
            }
        ),
        (
            card.motionSync,
            'card.motion.sync',
            {
                'start': True,
                'stop': False,
                'minutes': 60,
                'count': 10,
                'threshold': 0
            }
        ),
        (
            card.motionTrack,
            'card.motion.track',
            {
                'start': True,
                'stop': False,
                'minutes': 120,
                'count': 15,
                'threshold': 0,
                'file': '_motion.qo',
                'now': True
            }
        ),
        (
            card.restart,
            'card.restart',
            {}
        ),
        (
            card.random,
            'card.random',
            {'mode': 'entropy', 'count': 16}
        ),
        (
            card.restore,
            'card.restore',
            {
                'delete': True,
                'connected': False
            }
        ),
        (
            card.sleep,
            'card.sleep',
            {
                'on': True,
                'off': False,
                'seconds': 60,
                'mode': 'accel'
            }
        ),
        (
            card.trace,
            'card.trace',
            {
                'mode': 'on'
            }
        ),
        (
            card.triangulate,
            'card.triangulate',
            {
                'mode': 'wifi,cell',
                'on': True,
                'usb': True,
                'set': True,
                'minutes': 30,
                'text': '+CWLAP:(4,"Blues",-51,"74:ac:b9:12:12:f8",1)\n',
                'time': 1606755042
            }
        ),
        (
            card.usageGet,
            'card.usage.get',
            {
                'mode': '1day',
                'offset': 5
            }
        ),
        (
            card.usageTest,
            'card.usage.test',
            {
                'days': 7,
                'hours': 12,
                'megabytes': 500
            }
        ),
        (
            card.wifi,
            'card.wifi',
            {
                'ssid': 'MyNetwork',
                'password': 'MyPassword',
                'name': 'ACME Inc',
                'org': 'ACME Inc',
                'start': True,
                'text': '["SSID1","PASS1"],["SSID2","PASS2"]'
            }
        ),
        (
            card.wirelessPenalty,
            'card.wireless.penalty',
            {
                'reset': True,
                'set': False,
                'rate': 2.0,
                'add': 10,
                'max': 720,
                'min': 5
            }
        ),
        (
            card.attn,
            'card.attn',
            {
                'off': True,
                'on': False
            }
        ),
        (
            card.dfu,
            'card.dfu',
            {
                'off': True,
                'on': False
            }
        ),
        (
            card.locationMode,
            'card.location.mode',
            {
                'delete': True
            }
        ),
        (
            card.temp,
            'card.temp',
            {
                'stop': True,
                'sync': False
            }
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'usb': True,
                'alert': False,
                'sync': True,
                'set': False
            }
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'on': True
            }
        ),
        (
            card.voltage,
            'card.voltage',
            {
                'off': True
            }
        ),
        (
            card.wireless,
            'card.wireless',
            {
                'hours': 24
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
