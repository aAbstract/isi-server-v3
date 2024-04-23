import requests
import json
import _test_util
import paho.mqtt.client as mqtt_client


def test_get_room_devices_lock():
    api_route = 'user/devices/get-room-devices'
    _test_util.assert_api_lock_invalid_token(api_route)


def test_get_device_lock():
    api_route = 'user/devices/get-device'
    _test_util.assert_api_lock_invalid_token(api_route)


def test_get_room_devices():
    api_route = 'user/devices/get-room-devices'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    _test_util.assert_api_get_struct(api_route, access_tokens, {'id', 'device_config', 'link_type', 'device_name', 'is_online', 'room_name', 'device_type'}, json_body={'room_name': 'living_room_0'})


def test_get_device_not_found():
    api_route = 'user/devices/get-device'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    _test_util.assert_api_fail_msg(api_route, access_tokens, 404, 'Device not Found', json_body={'device_name': 'fake_device_name'})


def test_get_device():
    api_route = 'user/devices/get-device'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    _test_util.assert_api_get_struct(api_route, access_tokens, {'device_type', 'is_online', 'room_name', 'id', 'device_config', 'link_type', 'device_name'}, json_body={'device_name': 'motion_sensor_0'})


def test_get_temp_humd_devices():
    api_route = 'user/devices/get-temp-humd-devices'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    devices = _test_util.assert_api_get_struct(api_route, access_tokens, {'device_type', 'is_online', 'room_name', 'id', 'device_config', 'link_type', 'device_name'})
    device_types = set([x['device_type'] for x in devices])
    assert device_types == {'TEMP', 'HUMD'}


def test_change_device_config_device_not_found():
    api_route = 'user/devices/change-device-config'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    _test_util.assert_api_fail_msg(api_route, access_tokens, 404, 'Device not Found', json_body={
        'device_name': 'fake_device',
        'config_name': '',
        'config_new_val': True,
    })


def test_change_device_config_config_name_not_found():
    api_route = 'user/devices/change-device-config'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    _test_util.assert_api_fail_msg(api_route, access_tokens, 400, 'Invalid config_name', json_body={
        'device_name': 'motion_sensor_0',
        'config_name': 'fake_config',
        'config_new_val': True,
    })


def test_change_device_config_success():
    api_route = 'user/devices/change-device-config'
    access_tokens = [
        _test_util.login_user('test_admin', 'TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        _test_util.login_user('test_user', 'upass123'),
    ]

    _test_util.assert_api_ok_msg(api_route, access_tokens, json_body={
        'device_name': 'motion_sensor_0',
        'config_name': 'sec_mode',
        'config_new_val': True,
    })


def _test_configure_device_lock():
    api_url = f"{_test_util.get_api_url()}/configure-device"
    http_headers = {'Authorization': 'Bearer fake_token'}
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 403)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')


def _test_configure_device():
    device_name = 'motion_sensor_8'
    config_param = 'sec_mode'
    config_val = 1
    admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
    http_headers = {'Authorization': f"Bearer {admin_access_token}"}

    # test device not found case
    api_url = f"{_test_util.get_api_url()}/configure-device"
    json_req = {
        'device_name': 'fake_device',
        config_param: config_val,
    }
    http_res = requests.post(api_url, headers=http_headers, json=json_req)
    assert http_res.status_code == 404
    json_res_body = json.loads(http_res.content.decode())
    assert not json_res_body['success']
    assert json_res_body['msg'] == 'Device Not Found'

    # test config not found case
    api_url = f"{_test_util.get_api_url()}/configure-device"
    json_req = {
        'device_name': device_name,
        'fake_config': config_val,
    }
    http_res = requests.post(api_url, headers=http_headers, json=json_req)
    assert http_res.status_code == 404
    json_res_body = json.loads(http_res.content.decode())
    assert not json_res_body['success']
    assert json_res_body['msg'] == 'Config Not Found'

    # test valid case
    # set new config
    api_url = f"{_test_util.get_api_url()}/configure-device"
    json_req = {
        'device_name': device_name,
        'sec_mode': config_val,
    }
    http_res = requests.post(api_url, headers=http_headers, json=json_req)
    assert http_res.status_code == 200
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert json_res_body['msg'] == 'OK'

    # validate new config
    api_url = f"{_test_util.get_api_url()}/get-room-devices"
    http_res = requests.post(api_url, headers=http_headers, json={'room_name': 'living_room_0'})
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert ('devices' in json_res_body['data'])
    if len(json_res_body['data']['devices']) > 0:
        target_device = list(filter(lambda x: x['device_name'] == device_name, json_res_body['data']['devices']))[0]
        assert target_device['config'][config_param] == config_val


def _test_mqtt_devices_state():
    device_name = 'some_device_name'
    device_state_recv_msg: str = None

    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal device_state_recv_msg
        if message.topic == f"state/{device_name}/main":
            device_state_recv_msg = message.payload.decode()

    # setup connection
    _mqtt_client = mqtt_client.Client(client_id='isi_server_test_mqtt_devices_state', clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(_test_util.SERVER_IP, keepalive=60)
    _mqtt_client.subscribe(f"state/{device_name}/main")
    _mqtt_client.on_message = mqtt_read_handler

    # update device state
    _mqtt_client.publish(f"state/{device_name}/main", '10', retain=True)

    # validate state update
    while not device_state_recv_msg:
        _mqtt_client.loop(0.1)
    assert device_state_recv_msg == '10'

    # validate retain flag
    device_state_recv_msg = None
    _mqtt_client.unsubscribe(f"state/{device_name}/main")
    _mqtt_client.subscribe(f"state/{device_name}/main")
    while not device_state_recv_msg:
        _mqtt_client.loop(0.1)
    assert device_state_recv_msg == '10'


def _test_mqtt_devices_cmd():
    device_name = 'some_device_name'
    device_cmd_recv_msg: str = None

    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal device_cmd_recv_msg
        if message.topic == f"command/{device_name}/power_0":
            device_cmd_recv_msg = message.payload.decode()

    # setup connection
    _mqtt_client = mqtt_client.Client(client_id='isi_server_test_mqtt_devices_cmd', clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(_test_util.SERVER_IP, keepalive=60)
    _mqtt_client.subscribe(f"command/{device_name}/power_0")
    _mqtt_client.on_message = mqtt_read_handler

    # send device cmd
    _mqtt_client.publish(f"command/{device_name}/power_0", 'ON')

    # validate cmd recv
    while not device_cmd_recv_msg:
        _mqtt_client.loop(0.1)
    assert device_cmd_recv_msg == 'ON'

    # validate retain flag
    counter = 0
    device_cmd_recv_msg = None
    _mqtt_client.unsubscribe(f"command/{device_name}/power_0")
    _mqtt_client.subscribe(f"command/{device_name}/power_0")
    while not device_cmd_recv_msg:
        _mqtt_client.loop(0.1)
        counter += 1
        if counter == 10:
            break
    assert device_cmd_recv_msg == None


def _test_sample_device_automation():
    automation_device_name = 'main_switch_0'
    trigger_device_name = 'motion_sensor_8'
    admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
    http_headers = {'Authorization': f"Bearer {admin_access_token}"}

    automation_recv_msg: str = None
    client_notif_recv_msg: str = None

    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal automation_recv_msg
        nonlocal client_notif_recv_msg
        if message.topic == f"command/{automation_device_name}/power_0":
            automation_recv_msg = message.payload.decode()
        elif message.topic == 'telem/client/notif':
            client_notif_recv_msg = message.payload.decode()

    # motion sensor [light_mode=1]
    # setup connection
    _mqtt_client = mqtt_client.Client(client_id='isi_server_test_sample_device_automation', clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(_test_util.SERVER_IP, keepalive=60)
    _mqtt_client.subscribe(f"command/{automation_device_name}/power_0")
    _mqtt_client.subscribe('telem/client/notif')
    _mqtt_client.on_message = mqtt_read_handler

    # set light_mode = 1
    api_url = f"{_test_util.get_api_url()}/configure-device"
    json_req = {
        'device_name': trigger_device_name,
        'light_mode': 1,
    }
    http_res = requests.post(api_url, headers=http_headers, json=json_req)
    assert http_res.status_code == 200
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert json_res_body['msg'] == 'OK'
    api_url = f"{_test_util.get_api_url()}/get-room-devices"
    http_res = requests.post(api_url, headers=http_headers, json={'room_name': 'living_room_0'})
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert ('devices' in json_res_body['data'])
    if len(json_res_body['data']['devices']) > 0:
        target_device = list(filter(lambda x: x['device_name'] == trigger_device_name, json_res_body['data']['devices']))[0]
        assert target_device['config']['light_mode'] == 1

    # trigger automation
    _mqtt_client.publish(f"telem/{trigger_device_name}/notif", 'MOTION')

    # validate automation
    while not automation_recv_msg:
        _mqtt_client.loop(0.1)
    assert automation_recv_msg == 'ON'

    # motion sensor [sec_mode]
    api_url = f"{_test_util.get_api_url()}/configure-device"
    json_req = {
        'device_name': trigger_device_name,
        'sec_mode': 1,
    }
    http_res = requests.post(api_url, headers=http_headers, json=json_req)
    assert http_res.status_code == 200
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert json_res_body['msg'] == 'OK'
    api_url = f"{_test_util.get_api_url()}/get-room-devices"
    http_res = requests.post(api_url, headers=http_headers, json={'room_name': 'living_room_0'})
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert ('devices' in json_res_body['data'])
    if len(json_res_body['data']['devices']) > 0:
        target_device = list(filter(lambda x: x['device_name'] == trigger_device_name, json_res_body['data']['devices']))[0]
        assert target_device['config']['sec_mode'] == 1

    # trigger automation
    _mqtt_client.publish(f"telem/{trigger_device_name}/notif", 'MOTION')

    # validate automation
    while not client_notif_recv_msg:
        _mqtt_client.loop(0.1)
    notif_msg_obj = json.loads(client_notif_recv_msg)
    assert set(notif_msg_obj.keys()) == {'device', 'msg_lvl', 'msg_body', 'room'}


def _test_get_device_info_lock():
    api_url = f"{_test_util.get_api_url()}/get-device-info"
    http_headers = {'Authorization': 'Bearer fake_token'}
    http_res = requests.post(api_url, headers=http_headers)
    assert (http_res.status_code == 403)
    json_res_body = json.loads(http_res.content.decode())
    assert (not json_res_body['success'] and json_res_body['msg'] == 'Unauthorized API Access [Invalid Token]')


def _test_get_device_info_api():
    admin_access_token = _test_util.login_user('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')

    # test device not exist case
    api_url = f"{_test_util.get_api_url()}/get-device-info"
    http_headers = {'Authorization': f"Bearer {admin_access_token}"}
    http_res = requests.post(api_url, headers=http_headers, json={'device_name': 'fake_device'})
    assert http_res.status_code == 404
    json_res_body = json.loads(http_res.content.decode())
    assert not json_res_body['success']
    assert json_res_body['msg'] == 'Device Not Found'

    # test valid case
    api_url = f"{_test_util.get_api_url()}/get-device-info"
    http_headers = {'Authorization': f"Bearer {admin_access_token}"}
    http_res = requests.post(api_url, headers=http_headers, json={'device_name': 'main_switch_0'})
    assert (http_res.status_code == 200)
    json_res_body = json.loads(http_res.content.decode())
    assert json_res_body['success']
    assert 'device' in json_res_body['data']
    target_device_obj_keys = {'device_type', 'device_name_symbol', 'link_type', 'is_online', 'room_name', 'room_id', 'device_name', 'config', 'config_templates', 'device_id'}
    device_obj_keys = set(json_res_body['data']['device'])
    assert target_device_obj_keys == device_obj_keys
