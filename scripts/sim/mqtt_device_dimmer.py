#!/usr/bin/python

import json
import paho.mqtt.client as mqtt_client
import mqtt_net_conf

# create fake device connection
device_state = 'OFF'
device_name = 'main_dimmer_13'
_mqtt_client = mqtt_client.Client(client_id=f"isi_device.{device_name}", clean_session=True, userdata=None)
mqtt_broker_ip = mqtt_net_conf.SERVER_IP


def broadcast_req_handler(msg: str):
    if msg == 'DEVICES_SCAN':
        print(f"Received MQTT scan request")
        _mqtt_client.publish(f"telem/{device_name}/DEVICE_LWT", 'ONLINE')


def command_req_handler(cmd_obj: dict):
    global device_state

    print(f"Executing command: {cmd_obj}")
    if cmd_obj['command'] == 'DIM_0':
        device_state = '0'
        print(f"Device new state: {device_state}")
        _mqtt_client.publish(f"state/{device_name}/main", device_state, retain=True)

    elif cmd_obj['command'] == 'DIM_1':
        device_state = '35'
        print(f"Device new state: {device_state}")
        _mqtt_client.publish(f"state/{device_name}/main", device_state, retain=True)

    elif cmd_obj['command'] == 'DIM_2':
        device_state = '70'
        print(f"Device new state: {device_state}")
        _mqtt_client.publish(f"state/{device_name}/main", device_state, retain=True)

    elif cmd_obj['command'] == 'DIM_3':
        device_state = '100'
        print(f"Device new state: {device_state}")
        _mqtt_client.publish(f"state/{device_name}/main", device_state, retain=True)

    elif cmd_obj['command'] == 'TOGGLE':
        device_state = 'ON' if device_state == 'OFF' else 'OFF'
        print(f"Device new state: {device_state}")
        _mqtt_client.publish(f"state/{device_name}/main", device_state, retain=True)


def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
    if message.topic == 'telem/broadcast':
        broadcast_req_handler(message.payload.decode())
    else:
        command_req_handler(json.loads(message.payload.decode()))


# connect to mqtt broker
_mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
_mqtt_client.connect(mqtt_broker_ip, keepalive=60)
_mqtt_client.subscribe('telem/broadcast')
_mqtt_client.subscribe(f"command/{device_name}/dimmer_1")
_mqtt_client.subscribe(f"command/{device_name}/power_1")
_mqtt_client.on_message = mqtt_read_handler
_mqtt_client.publish(f"state/{device_name}/main", device_state, retain=True)


print(f"MQTT device {device_name} online")
while True:
    _mqtt_client.loop(0.1)
