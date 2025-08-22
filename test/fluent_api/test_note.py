import pytest
from notecard import note


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            note.add,
            'note.add',
            {
                'file': 'data.qo',
                'body': {'key_a:', 'val_a', 'key_b', 42},
                'payload': 'ewogICJpbnRlcnZhbHMiOiI2MCwxMiwxNCIKfQ==',
                'sync': True
            },
        ),
        (
            note.add,
            'note.add',
            {
                'note': 'test_note_id',
                'key': 'encryption_key',
                'verify': True,
                'binary': True,
                'live': True,
                'full': True,
                'limit': True,
                'max': 100
            },
        ),
        (
            note.changes,
            'note.changes',
            {
                'file': 'my-settings.db',
                'tracker': 'inbound-tracker',
                'max': 2,
                'start': True,
                'stop': True,
                'delete': True,
                'deleted': True
            },
        ),
        (
            note.changes,
            'note.changes',
            {
                'file': 'my-settings.db',
                'reset': True
            },
        ),
        (
            note.delete,
            'note.delete',
            {
                'file': 'my-settings.db',
                'note': 'my_note',
            },
        ),
        (
            note.delete,
            'note.delete',
            {
                'file': 'my-settings.db',
                'note': 'my_note',
                'verify': True
            },
        ),
        (
            note.get,
            'note.get',
            {
                'file': 'my-settings.db',
                'note': 'my_note',
                'delete': True,
                'deleted': True
            },
        ),
        (
            note.get,
            'note.get',
            {
                'file': 'my-settings.db',
                'decrypt': True
            },
        ),
        (
            note.template,
            'note.template',
            {
                'file': 'my-settings.db',
                'body': {'key_a:', 'val_a', 'key_b', 42},
                'length': 42,
                'format': "compact"
            },
        ),
        (
            note.template,
            'note.template',
            {
                'file': 'my-settings.db',
                'verify': True,
                'port': 1,
                'delete': True
            },
        ),
        (
            note.update,
            'note.update',
            {
                'file': 'my-settings.db',
                'note': 'my_note',
                'body': {'key_a:', 'val_a', 'key_b', 42},
                'payload': 'ewogICJpbnRlcnZhbHMiOiI2MCwxMiwxNCIKfQ=='
            },
        ),
        (
            note.update,
            'note.update',
            {
                'file': 'my-settings.db',
                'note': 'my_note',
                'verify': True
            },
        )
    ]
)
class TestNote:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params, run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params, run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
