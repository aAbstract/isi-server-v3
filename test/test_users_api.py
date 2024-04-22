# import jwt
# import requests
# import json
# import _test_util

def test_todo():
    pass

# def test_get_users_lock():
#     # test fake token case
#     api_url = f"{_test_util.get_api_url()}/admin-get-users"
#     http_headers = {'Authorization': 'Bearer fake_token'}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert (http_res.status_code == 403)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')

#     # test real USER token lock
#     user_access_token = _test_util.login_user('test_user', 'test_user_pass_123')
#     http_headers = {'Authorization': f"Bearer {user_access_token}"}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert (http_res.status_code == 403)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Restricted Access]')


# def test_get_users():
#     api_url = f"{_test_util.get_api_url()}/admin-get-users"
#     admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
#     http_headers = {'Authorization': f"Bearer {admin_access_token}"}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert http_res.status_code == 200
#     json_res_body = json.loads(http_res.content.decode())
#     assert json_res_body['success']
#     assert ('users' in json_res_body['data'])
#     if len(json_res_body['data']['users']) > 0:
#         user_obj_keys = {'username', 'role', 'full_name', 'is_online', 'user_id'}
#         assert set(json_res_body['data']['users'][0].keys()) == user_obj_keys


# def test_update_user_lock():
#     api_url = f"{_test_util.get_api_url()}/update-user"
#     http_headers = {'Authorization': 'Bearer fake_token'}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert (http_res.status_code == 403)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')


# def test_user_update_other_user_lock():
#     # TODO
#     pass


# def test_user_update_admin_lock():
#     # TODO
#     pass


# def test_user_update_user():
#     # user do not exists case
#     username = 'test_user'
#     api_url = f"{_test_util.get_api_url()}/update-user"
#     user_access_token = _test_util.login_user(username, 'test_user_pass_123')
#     http_headers = {'Authorization': f"Bearer {user_access_token}"}
#     http_res = requests.post(api_url, headers=http_headers, json={'username': 'fake_user', 'full_name': 'New Full Name'})
#     assert http_res.status_code == 404
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'User Not Found')

#     # invalid update key case
#     http_res = requests.post(api_url, headers=http_headers, json={'username': username, 'fake_key': 'fake_value'})
#     assert http_res.status_code == 400
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Invalid Update Key')

#     # valid update case
#     http_res = requests.post(api_url, headers=http_headers, json={'username': username, 'full_name': 'New Full Name'})
#     assert http_res.status_code == 200
#     json_res_body = json.loads(http_res.content.decode())
#     assert json_res_body['success']
#     token_claims = jwt.decode(json_res_body['data']['access_token'], options={'verify_signature': False})
#     assert token_claims['full_name'] == 'New Full Name'

#     # revert changes
#     http_res = requests.post(api_url, headers=http_headers, json={'username': username, 'full_name': 'Test User'})
#     assert http_res.status_code == 200
#     json_res_body = json.loads(http_res.content.decode())
#     assert json_res_body['success']
#     token_claims = jwt.decode(json_res_body['data']['access_token'], options={'verify_signature': False})
#     assert token_claims['full_name'] == 'Test User'


# def test_admin_update_user():
#     # TODO
#     pass


# def test_admin_add_user_api_lock():
#     # test fake token case
#     api_url = f"{_test_util.get_api_url()}/admin-create-user"
#     http_headers = {'Authorization': 'Bearer fake_token'}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert (http_res.status_code == 403)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')

#     # test real USER token lock
#     user_access_token = _test_util.login_user('test_user', 'test_user_pass_123')
#     http_headers = {'Authorization': f"Bearer {user_access_token}"}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert (http_res.status_code == 403)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Restricted Access]')


# def test_admin_add_user_api():
#     # test invalid user object case
#     api_url = f"{_test_util.get_api_url()}/admin-create-user"
#     admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
#     http_headers = {'Authorization': f"Bearer {admin_access_token}"}
#     http_res = requests.post(api_url, headers=http_headers)
#     assert (http_res.status_code == 400)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Invalid User Object')

#     # user already exists case
#     user_obj = {
#         'username': 'test_admin',
#         'full_name': 'Test Admin',
#         'password': '1234',
#     }
#     json_req_body = {'user': user_obj}
#     http_res = requests.post(api_url, headers=http_headers, json=json_req_body)
#     assert (http_res.status_code == 400)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (not json_res_body['success'] and json_res_body['msg'] == 'Username Already Exists')

#     # valid user object case
#     user_obj = {
#         'username': 'test_add_user',
#         'full_name': 'Test Add User',
#         'password': '1234',
#     }
#     json_req_body = {'user': user_obj}
#     http_res = requests.post(api_url, headers=http_headers, json=json_req_body)
#     assert http_res.status_code == 200
#     json_res_body = json.loads(http_res.content.decode())
#     assert (json_res_body['success'] and json_res_body['msg'] == 'OK')
#     assert 'user_id' in json_res_body['data']

#     # validate
#     user_id: int = json_res_body['data']['user_id']
#     api_url = f"{_test_util.get_api_url()}/admin-get-users"
#     http_res = requests.post(api_url, headers=http_headers)
#     assert http_res.status_code == 200
#     json_res_body = json.loads(http_res.content.decode())
#     assert json_res_body['success']
#     assert ('users' in json_res_body['data'])
#     users: list[dict] = json_res_body['data']['users']
#     mactched_user = list(filter(lambda x: x['user_id'] == user_id, users))
#     assert mactched_user
#     mactched_user = mactched_user[0]
#     assert mactched_user == {
#         'user_id': user_id,
#         'username': 'test_add_user',
#         'full_name': 'Test Add User',
#         'role': 'USER',
#         'is_online': False,
#     }

#     # remove side effects
#     username: str = mactched_user['username']
#     api_url = f"{_test_util.get_api_url()}/admin-delete-user"
#     http_res = requests.post(api_url, headers=http_headers, json={'username': username})
#     assert (http_res.status_code == 200)
#     json_res_body = json.loads(http_res.content.decode())
#     assert (json_res_body['success'] and json_res_body['msg'] == 'OK')
