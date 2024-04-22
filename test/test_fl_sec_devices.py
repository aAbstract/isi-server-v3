import json
import _test_util
import paho.mqtt.client as mqtt_client


def _test_notif_automation(device_name: str, msg: str):
    client_notif_recv_msg: str = None

    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal client_notif_recv_msg
        if message.topic == 'telem/client/notif':
            client_notif_recv_msg = message.payload.decode()

    # setup connection
    _mqtt_client = mqtt_client.Client(client_id='isi_server_test_sample_device_automation', clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(_test_util.SERVER_IP, keepalive=60)
    _mqtt_client.subscribe('telem/client/notif')
    _mqtt_client.on_message = mqtt_read_handler

    # trigger automation
    _mqtt_client.publish(f"telem/{device_name}/notif", msg)

    # validate automation
    while not client_notif_recv_msg:
        _mqtt_client.loop(0.1)
    notif_msg_obj = json.loads(client_notif_recv_msg)
    assert set(notif_msg_obj.keys()) == {'device', 'msg_lvl', 'msg_body', 'room'}


def test_flood_sensor_automation():
    _test_notif_automation('flood_sensor_0', 'FLOOD')


def test_sec_lock_sensor_automation():
    _test_notif_automation('security_lock_0', 'UNLOCKED')
