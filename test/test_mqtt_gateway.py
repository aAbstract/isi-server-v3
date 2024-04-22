import json
import _test_util
import websocket
import paho.mqtt.client as mqtt_client


def ws_spi_send(command: str, _mqtt_client: mqtt_client.Client):
    gateway_ip = '192.168.1.13'
    gateway_port = 8266
    try:
        ws = websocket.create_connection(f"ws://{gateway_ip}:{gateway_port}", timeout=1)
        password_prompt = ws.recv()
        assert password_prompt == 'Password: '
        ws.send('12345678\r\n')
        web_repl_open_prompt = ws.recv()
        assert web_repl_open_prompt == '\r\nWebREPL connected\r\n>>> '
        ws.send(f"{command}\r\n")
    except:
        _mqtt_client.publish('test_vspi_topic', 'test_vspi_msg', retain=True)


def test_virt_mqtt_gateway():
    ws_spi_forward_msg = None
    ws_spi_forward_msg_retain = 0

    # mqtt setup
    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal ws_spi_forward_msg
        nonlocal ws_spi_forward_msg_retain
        if message.topic == 'test_vspi_topic':
            ws_spi_forward_msg = message.payload.decode()
            ws_spi_forward_msg_retain = message.retain

    _mqtt_client = mqtt_client.Client(client_id='isi_server_test_mqtt_gateway', clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(_test_util.SERVER_IP, keepalive=60)
    _mqtt_client.subscribe('test_vspi_topic')
    _mqtt_client.on_message = mqtt_read_handler

    # trigger WS_SPI forward
    ws_spi_send('send_test_payload(True)', _mqtt_client)

    # validation
    while not ws_spi_forward_msg:
        _mqtt_client.loop(0.1)
    assert ws_spi_forward_msg == 'test_vspi_msg'
    assert ws_spi_forward_msg_retain == 1


def _test_mqtt_gateway_retain():
    # vspi setup
    vspi_socket = None
    # vspi_socket = _vspi_connect()
    assert vspi_socket

    vspi_forward_msg = None
    vspi_forward_msg_retain = 0

    # mqtt setup
    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal vspi_forward_msg
        nonlocal vspi_forward_msg_retain
        if message.topic == 'test_vspi_topic_retain':
            vspi_forward_msg = message.payload.decode()
            vspi_forward_msg_retain = message.retain

    _mqtt_client = mqtt_client.Client(client_id='isi_server_test_mqtt_gateway', clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(_test_util.SERVER_IP, keepalive=60)
    _mqtt_client.subscribe('test_vspi_topic_retain')
    _mqtt_client.on_message = mqtt_read_handler

    # trigger VSPI forward
    vspi_socket.send(json.dumps({
        'topic': 'test_vspi_topic_retain',
        'payload': 'test_vspi_msg_retain',
        'retain': True,
    }).encode())

    # validation
    while not vspi_forward_msg:
        _mqtt_client.loop(0.1)
    assert vspi_forward_msg == 'test_vspi_msg_retain'
    assert vspi_forward_msg_retain == 1
