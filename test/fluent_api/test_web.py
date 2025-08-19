import pytest
from notecard import web


@pytest.mark.parametrize(
    'fluent_api,notecard_api,req_params,rename_key_map',
    [
        (
            web.delete,
            'web.delete',
            {
                'route': 'my-proxy-route',
                'name': '/api/delete',
                'content': 'application/json',
                'seconds': 30,
                'async_': True,
                'file': 'responses.dbx',
                'note': 'delete_response_1'
            },
            {
                'async_': 'async'
            }
        ),
        (
            web.get,
            'web.get',
            {
                'route': 'my-proxy-route',
                'name': '/api/data',
                'body': {'key': 'value'},
                'content': 'application/json',
                'seconds': 60,
                'async_': False,
                'binary': True,
                'offset': 0,
                'max': 1024,
                'file': 'responses.dbx',
                'note': 'get_response_1'
            },
            {
                'async_': 'async'
            }
        ),
        (
            web.post,
            'web.post',
            {
                'route': 'my-proxy-route',
                'name': '/api/submit',
                'body': {'sensor': 'temperature', 'value': 23.5},
                'payload': 'ewogICJkYXRhIjogImV4YW1wbGUiCn0=',
                'content': 'application/json',
                'seconds': 45,
                'total': 2048,
                'offset': 512,
                'status': 'pending',
                'max': 1024,
                'verify': True,
                'async_': False,
                'binary': False,
                'file': 'responses.dbx',
                'note': 'post_response_1'
            },
            {
                'async_': 'async'
            }
        ),
        (
            web.put,
            'web.put',
            {
                'route': 'my-proxy-route',
                'name': '/api/update',
                'body': {'id': 123, 'status': 'updated'},
                'payload': 'ewogICJ1cGRhdGVkIjogdHJ1ZQp9',
                'content': 'application/json',
                'seconds': 90,
                'total': 4096,
                'offset': 1024,
                'status': 'complete',
                'max': 2048,
                'verify': False,
                'async_': True,
                'file': 'responses.dbx',
                'note': 'put_response_1'
            },
            {
                'async_': 'async'
            }
        ),
        (
            web.web,
            'web',
            {
                'route': 'my-proxy-route',
                'method': 'GET',
                'name': '/api/status',
                'content': 'text/plain'
            },
            None
        )
    ]
)
class TestWeb:
    def test_fluent_api_maps_notecard_api_correctly(
            self, fluent_api, notecard_api, req_params, rename_key_map,
            run_fluent_api_notecard_api_mapping_test):
        run_fluent_api_notecard_api_mapping_test(fluent_api, notecard_api,
                                                 req_params, rename_key_map)

    def test_fluent_api_fails_with_invalid_notecard(
            self, fluent_api, notecard_api, req_params, rename_key_map,
            run_fluent_api_invalid_notecard_test):
        run_fluent_api_invalid_notecard_test(fluent_api, req_params, rename_key_map)
