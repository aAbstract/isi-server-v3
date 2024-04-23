import requests


SERVER_IP = '127.0.0.1'
HTTP_PORT = 8080


def get_api_url():
    return f"http://{SERVER_IP}:{HTTP_PORT}/api"


def login_user(username: str, password: str) -> str:
    api_url = f"{get_api_url()}/auth/login"
    http_res = requests.post(api_url, data={
        'username': username,
        'password': password,
    })
    json_res = http_res.json()
    return json_res['access_token']


def assert_api_lock_invalid_token(route: str):
    api_url = f"{get_api_url()}/{route}"
    http_headers = {'Authorization': 'Bearer fake_token'}
    http_res = requests.post(api_url, headers=http_headers)
    assert http_res.status_code == 403
    json_res = http_res.json()
    json_res['detail'] == 'Unauthorized API Access [Invalid Token]'


def assert_api_lock_restricted_access(route: str):
    api_url = f"{get_api_url()}/{route}"
    user_access_token = login_user('dev_user', 'QzznLwAuRoibiyJG5iXd7BAFDzuGA36f')
    http_headers = {'Authorization': f"Bearer {user_access_token}"}
    http_res = requests.post(api_url, headers=http_headers)
    assert http_res.status_code == 403
    json_res = http_res.json()
    json_res['detail'] == 'Unauthorized API Access [Restricted Access]'


def assert_api_get_struct(route: str, access_tokens: list[str], target_keys: set[str], json_body: dict = {}) -> list:
    api_url = f"{get_api_url()}/{route}"
    for access_token in access_tokens:
        http_headers = {'Authorization': f"Bearer {access_token}"}
        http_res = requests.post(api_url, headers=http_headers, json=json_body)
        assert http_res.status_code == 200
        items: list = http_res.json()
        if len(items) > 0:
            obj_keys = set(items[0].keys())
            assert obj_keys == target_keys
        return items


def assert_api_fail_msg(route: str, access_tokens: list[str], target_status_code: int, target_msg: str, json_body: dict = {}):
    api_url = f"{get_api_url()}/{route}"
    for access_token in access_tokens:
        http_headers = {'Authorization': f"Bearer {access_token}"}
        http_res = requests.post(api_url, headers=http_headers, json=json_body)
        assert http_res.status_code == target_status_code
        json_res = http_res.json()
        assert json_res['detail'] == target_msg


def assert_api_ok_msg(route: str, access_tokens: list[str], json_body: dict = {}):
    api_url = f"{get_api_url()}/{route}"
    for access_token in access_tokens:
        http_headers = {'Authorization': f"Bearer {access_token}"}
        http_res = requests.post(api_url, headers=http_headers, json=json_body)
        assert http_res.status_code == 200
        assert http_res.json() == 'OK'
