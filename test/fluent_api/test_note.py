import pytest
from notecard import note


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params,rename_key_map,rename_value_map',
    [
        (
            note.add,
            'note.add',
            {
                'file': 'data.qo',
                'body': {'key_a:', 'val_a', 'key_b', 42},
                'payload': 'ewogICJpbnRlcnZhbHMiOiI2MCwxMiwxNCIKfQ==',
                'port': 50,
                'sync': True
            },
            None,
            None
        ),
        (
            note.changes,
            'note.changes',
            {
                'file': 'my-settings.db',
                'tracker': 'inbound-tracker',
                'maximum': 2,
                'start': True,
                'stop': True,
                'delete': True,
                'deleted': True
            },
            {
                'maximum': 'max'
            },
            None
        ),
        (
            note.delete,
            'note.delete',
            {
                'file': 'my-settings.db',
                'note_id': 'my_note',
            },
            {
                'note_id': 'note'
            },
            None
        ),
        (
            note.get,
            'note.get',
            {
                'file': 'my-settings.db',
                'note_id': 'my_note',
                'delete': True,
                'deleted': True
            },
            {
                'note_id': 'note'
            },
            None
        ),
        (
            note.template,
            'note.template',
            {
                'file': 'my-settings.db',
                'body': {'key_a:', 'val_a', 'key_b', 42},
                'length': 42,
                'port': 50,
                'compact': True
            },
            {
                'compact': 'format'
            },
            {
                'format': 'compact'
            }
        ),
        (
            note.update,
            'note.update',
            {
                'file': 'my-settings.db',
                'note_id': 'my_note',
                'body': {'key_a:', 'val_a', 'key_b', 42},
                'payload': 'ewogICJpbnRlcnZhbHMiOiI2MCwxMiwxNCIKfQ=='
            },
            {
                'note_id': 'note'
            },
            None
        )
    ]
)
class TestNote:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params, rename_key_map,
            rename_value_map, run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params, rename_key_map,
                                                 rename_value_map)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params, rename_key_map,
            rename_value_map, run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params,
                                             rename_key_map, rename_value_map)
