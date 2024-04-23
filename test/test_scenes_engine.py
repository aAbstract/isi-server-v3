import json
import requests
import _test_util


def test_get_scenes_metadata_lock():
    api_route = 'user/scenes/get-scenes-metadata'
    _test_util.assert_api_lock_invalid_token(api_route)


def test_get_scene_lock():
    api_route = 'user/scenes/get-scene'
    _test_util.assert_api_lock_invalid_token(api_route)


def test_get_scenes_metadata():
    api_route = 'user/scenes/get-scenes-metadata'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]
    _test_util.assert_api_get_struct(api_route, access_tokens, {'scene_disp_name', 'id'})


def test_get_scene_not_found():
    api_route = 'user/scenes/get-scene'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]
    _test_util.assert_api_fail_msg(api_route, access_tokens, 404, 'Scene not Found', json_body={'scene_id': 'fake_scene_id'})


def test_get_scene():
    api_route = 'user/scenes/get-scene'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    # get example scene id
    http_headers = {'Authorization': f"Bearer {access_tokens[1]}"}
    http_res = requests.post(f'{_test_util.get_api_url()}/user/scenes/get-scenes-metadata', headers=http_headers)
    json_res = http_res.json()
    scene_id = json_res[0]['id']

    _test_util.assert_api_get_struct(api_route, access_tokens, {'scene_disp_name', 'id', 'actions'}, json_body={'scene_id': scene_id})


def test_sample_scene_automation():
    # TODO
    pass


def _test_create_scene_lock():
    api_url = f'{_test_util.get_api_url()}/create-scene'
    http_headers = {'Authorization': 'Bearer fake_token'}
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 403)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')


def _test_update_scene_lock():
    api_url = f'{_test_util.get_api_url()}/update-scene'
    http_headers = {'Authorization': 'Bearer fake_token'}
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 403)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')


def _test_delete_scene_lock():
    api_url = f'{_test_util.get_api_url()}/delete-scene'
    http_headers = {'Authorization': 'Bearer fake_token'}
    http_res = requests.post(api_url, headers=http_headers, json={'scene_name': 'fake_scene'})
    assert (http_res.status_code == 403)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')


def _test_update_scene_scene_not_exist():
    admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
    api_url = f'{_test_util.get_api_url()}/update-scene'
    http_headers = {'Authorization': f'Bearer {admin_access_token}'}
    scene_obj = {
        'scene_id': 0,
        'scene_name': 'fake_scene',
        'scene_name_fixed_symbol': 'Scene',
        'actions': [],
    }
    http_res = requests.post(api_url, headers=http_headers, json=scene_obj)
    assert (http_res.status_code == 404)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Scene Not Found')


def _test_delete_scene_scene_not_exist():
    admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
    api_url = f'{_test_util.get_api_url()}/delete-scene'
    http_headers = {'Authorization': f'Bearer {admin_access_token}'}
    scene_obj = {
        'scene_id': 0,
        'scene_name': 'fake_scene',
        'scene_name_fixed_symbol': 'Scene',
        'actions': [],
    }
    http_res = requests.post(api_url, headers=http_headers, json=scene_obj)
    assert (http_res.status_code == 404)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Scene Not Found')


def _test_scene_object_routine():
    # test create routine
    admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
    api_url = f'{_test_util.get_api_url()}/create-scene'
    http_headers = {'Authorization': f'Bearer {admin_access_token}'}
    scene_actions = [
        {
            'device_name': 'main_switch_0',
            'device_pref': 'power_1',
            'payload': '{}',
        },
        {
            'device_name': 'main_switch_0',
            'device_pref': 'power_2',
            'payload': '{}',
        },
        {
            'device_name': 'main_switch_0',
            'device_pref': 'power_3',
            'payload': '{}',
        },
    ]
    scene_obj = {'scene_name_fixed_symbol': 'Scene', 'actions': scene_actions}
    http_res = requests.post(api_url, headers=http_headers, json=scene_obj)
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert (json_res_body['success'] and json_res_body['msg'] == 'OK')
    assert 'scene_id' in json_res_body['data']

    # validate system state
    api_url = f'{_test_util.get_api_url()}/get-scenes'
    scene_id: int = json_res_body['data']['scene_id']
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    scenes: list[dict] = json_res_body['data']['scenes']
    mactched_scene = list(filter(lambda x: x['scene_id'] == scene_id, scenes))
    assert mactched_scene
    mactched_scene = mactched_scene[0]
    assert mactched_scene == {
        'scene_id': scene_id,
        'scene_name': f"scene_{scene_id}",
        'scene_name_fixed_symbol': 'Scene',
        'actions': scene_actions,
    }

    # test update routine
    api_url = f'{_test_util.get_api_url()}/update-scene'
    mactched_scene['actions'][0]['device_name'] = 'updated_device'
    http_res = requests.post(api_url, headers=http_headers, json=mactched_scene)
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert (json_res_body['success'] and json_res_body['msg'] == 'OK')

    # validate system state
    api_url = f'{_test_util.get_api_url()}/get-scenes'
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    scenes: list[dict] = json_res_body['data']['scenes']
    mactched_scene = list(filter(lambda x: x['scene_id'] == scene_id, scenes))
    assert mactched_scene
    mactched_scene = mactched_scene[0]
    assert mactched_scene['actions'][0]['device_name'] == 'updated_device'

    # remove side effects
    api_url = f'{_test_util.get_api_url()}/delete-scene'
    scene_name: str = mactched_scene['scene_name']
    http_res = requests.post(api_url, headers=http_headers, json={'scene_name': scene_name})
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert (json_res_body['success'] and json_res_body['msg'] == 'OK')

    # validate system state
    api_url = f'{_test_util.get_api_url()}/get-scenes'
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    scenes: list[dict] = json_res_body['data']['scenes']
    mactched_scene = list(filter(lambda x: x['scene_id'] == scene_id, scenes))
    assert not mactched_scene
