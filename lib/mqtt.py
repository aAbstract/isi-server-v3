import os
import logging
import paho.mqtt.client as mqtt_client


_mqtt_client = mqtt_client.Client(client_id='isi_server', clean_session=True, userdata=None)
_ISI_MQTT_LOG_TOPIC = 'telem/isi_mqtt_log'


def _isi_server_mqtt_handler(_1, _2, message: mqtt_client.MQTTMessage):
    if message.topic == _ISI_MQTT_LOG_TOPIC:
        logging.getLogger('uvicorn').info(f"MQTT-LOG: {message.payload.decode()}")


def mqtt_connect():
    try:
        _mqtt_client.username_pw_set(os.environ['MQTT_BROKER_USERNAME'], os.environ['MQTT_BROKER_PASSWORD'])
        _mqtt_client.connect(os.environ['MQTT_BROKER_IP'])
        _mqtt_client.subscribe(_ISI_MQTT_LOG_TOPIC)
        _mqtt_client.on_message = _isi_server_mqtt_handler
        _mqtt_client.loop_start()
        logging.getLogger('uvicorn').info(f"Connected to MQTT Broker: mqtt://{os.environ['MQTT_BROKER_IP']}")
    except Exception as e:
        logging.getLogger('uvicorn').error(f"Error connecting to MQTT Broker: mqtt://{os.environ['MQTT_BROKER_IP']}, Error: {e}")


def mqtt_disconnect():
    _mqtt_client.loop_stop()
    logging.getLogger('uvicorn').info('Disconnected from MQTT Broker')
