import pytest
from notecard import file


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params',
    [
        (
            file.changes,
            'file.changes',
            {
                'tracker': 'tracker',
                'files': ['file_1', 'file_2', 'file_3']
            }
        ),
        (
            file.delete,
            'file.delete',
            {
                'files': ['file_1', 'file_2', 'file_3']
            }
        ),
        (
            file.stats,
            'file.stats',
            {}
        ),
        (
            file.pendingChanges,
            'file.changes.pending',
            {}
        )
    ]
)
class TestFile:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params)
