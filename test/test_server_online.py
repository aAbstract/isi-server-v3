import requests
import _test_util


def test_server_online():
    api_url = f"{_test_util.get_api_url()}/test"
    http_res = requests.get(api_url)
    assert http_res.status_code == 200
    assert http_res.json() == 'SERVER_ONLINE'
