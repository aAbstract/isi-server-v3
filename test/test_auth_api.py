import requests
import _test_util


def test_auth_login_failed_invalid_account():
    api_url = f"{_test_util.get_api_url()}/auth/login"
    http_res = requests.post(api_url, data={
        'username': 'fake_user',
        'password': 'fake_password',
    })
    assert http_res.status_code == 401
    json_res = http_res.json()
    json_res['detail'] == 'Login Failed, Invalid User Credentials'


def test_auth_login_failed_invalid_password():
    api_url = f"{_test_util.get_api_url()}/auth/login"
    http_res = requests.post(api_url, data={
        'username': 'test_user',
        'password': 'fake_password',
    })
    assert http_res.status_code == 401
    json_res = http_res.json()
    json_res['detail'] == 'Login Failed, Invalid User Credentials'


def test_auth_login_success():
    api_url = f"{_test_util.get_api_url()}/auth/login"
    http_res = requests.post(api_url, data={
        'username': 'test_user',
        'password': 'upass123',
    })
    assert http_res.status_code == 200
    json_res = http_res.json()
    assert 'access_token' in json_res
