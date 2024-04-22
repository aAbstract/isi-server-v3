import time
import json
import requests
import socket
import colorama
import paho.mqtt.client as mqtt_client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


SERVER_IP = '192.168.122.17'
# SERVER_IP = '192.168.1.100'
HTTP_PORT = 1880
TCP_MQTT_PORT = 1881
WS_MQTT_PORT = 9001

CLIENT_DEV_SERVER_IP = '127.0.0.1'
CLIENT_DEV_SERVER_PORT = 5173

WDIWV = 0.1  # web driver implicit wait time in seconds
ANIMATION_DELAY = 3 * WDIWV
HTTP_DELAY = WDIWV
MQTT_DELAY = WDIWV

TESTING_ROOM_NAME = 'Living Room'
CHECK_MODE = 'IDLE'

# test devices info
SWITCH_DEVICE_INDEX = 0
PLUG_DEVICE_INDEX = 4
DIMMER_DEVICE_INDEX = 13
TEMP_DEVICE_INDEX = 3
HUMD_DEVICE_INDEX = 2
MOTION_DEVICE_INDEX = 8
FL_DEVICE_INDEX = 7
SL_DEVICE_INDEX = 6
SWITCH_DEVICE_NAME = f"main_switch_{SWITCH_DEVICE_INDEX}"
DIMMER_DEVICE_NAME = F"main_dimmer_{DIMMER_DEVICE_INDEX}"
TEMP_DEVICE_NAME = f"temperature_sensor_{TEMP_DEVICE_INDEX}"
HUMD_DEVICE_NAME = f"humidity_sensor_{HUMD_DEVICE_INDEX}"
MOTION_DEVICE_NAME = f"motion_sensor_{MOTION_DEVICE_INDEX}"
FL_DEVICE_NAME = f"flood_sensor_{FL_DEVICE_INDEX}"
SL_DEVICE_NAME = f"security_lock_{SL_DEVICE_INDEX}"


def elog(func_id: str, msg: str):
    err_tag = f"{colorama.Fore.RED}[ERROR]{colorama.Style.RESET_ALL}"
    print(f"{err_tag} {func_id} | {msg}")


def ilog(func_id: str, msg: str):
    info_tag = f"{colorama.Fore.GREEN}[INFO]{colorama.Style.RESET_ALL}"
    print(f"{info_tag} {func_id} | {msg}")


def is_port_open(host: str, port: int) -> bool:
    try:
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.settimeout(2)
        _socket.connect((host, port))
        return True
    except:
        return False
    finally:
        _socket.close()


def js_click(driver: webdriver.Chrome, btn):
    driver.execute_script('arguments[0].click();', btn)


def reset_app(driver: webdriver.Chrome):
    driver.get(f"http://{CLIENT_DEV_SERVER_IP}:{CLIENT_DEV_SERVER_PORT}/#/login")


def bottom_bar_click(driver: webdriver.Chrome, btn_lbl: str):
    bot_bar_btns = driver.find_elements(By.CSS_SELECTOR, '.mobile_bot_bar_icon_cont')
    target_btn = [x for x in bot_bar_btns if x.text == btn_lbl][0]
    js_click(driver, target_btn)


def get_elem_txt(elem: WebElement, css_selector: str) -> str | None:
    try:
        txt_elem = elem.find_element(By.CSS_SELECTOR, css_selector)
        return txt_elem.text
    except:
        return None


def load_room_devices(driver: webdriver.Chrome, room_name: str, func_id: str) -> list[WebElement] | None:
    room_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_rooms_card_grid_sec')
    living_room_card = [card for card in room_cards if card.text == room_name][0]
    js_click(driver, living_room_card)
    # validate
    device_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_room_card')
    if len(device_cards) == 0:
        elog(func_id, f"Room [{room_name}] Does not Have any Devices")
        return None

    return device_cards


def try_get_elem_txt(driver: webdriver.Chrome, css_selector: str) -> str | None:
    TIME_OUT = 100
    for _ in range(TIME_OUT):
        try:
            elem = driver.find_element(By.CSS_SELECTOR, css_selector)
            if elem.text != '':
                return elem.text
        except:
            pass

    return None


def try_get_elem_txts(driver: webdriver.Chrome, css_selector: str) -> list[str] | None:
    TIME_OUT = 100
    elems_txt = []

    def _try_get_elem_txt(elem: WebElement) -> str | None:
        for _ in range(TIME_OUT):
            try:
                if elem.text != '':
                    return elem.text
            except:
                pass

        return None

    for _ in range(TIME_OUT):
        try:
            elems = driver.find_elements(By.CSS_SELECTOR, css_selector)
            elems_txt = [_try_get_elem_txt(elem) for elem in elems]
            if None not in elems_txt:
                return elems_txt
        except:
            pass

    return None


def try_get_elem(driver: webdriver.Chrome, css_selector: str) -> WebElement | None:
    TIME_OUT = 100
    for _ in range(TIME_OUT):
        try:
            elem = driver.find_element(By.CSS_SELECTOR, css_selector)
            return elem
        except:
            pass

    return None


def publish_mqtt_msg(topic: str, payload: str):
    _mqtt_client = mqtt_client.Client(client_id=f"isi_e2e_script", clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(SERVER_IP, keepalive=60)
    _mqtt_client.publish(topic, payload)

    _mqtt_client.disconnect()
    del _mqtt_client


def read_mqtt_msg(func_id: str, topic: str, timeout: int = 10) -> str | None:
    _mqtt_client = mqtt_client.Client(client_id=f"isi_e2e_script", clean_session=True, userdata=None)
    _mqtt_client.username_pw_set('isi_muser', 'oE74zxUFEY35JX5ffyx4zUZTSauYS2zCFVhvL6gZe5bsBCQo3tP2pCS5VrH98mvX')
    _mqtt_client.connect(SERVER_IP, keepalive=60)
    _mqtt_client.subscribe(topic)

    recv_msg = None

    def mqtt_read_handler(_1, _2, message: mqtt_client.MQTTMessage):
        nonlocal recv_msg
        if message.topic == topic:
            recv_msg = message.payload.decode()
    _mqtt_client.on_message = mqtt_read_handler

    i = 0
    while not recv_msg:
        _mqtt_client.loop(0.1)
        i += 1
        time.sleep(0.1)
        if i >= timeout:
            elog(func_id, f"MQTT Read Timeout, timeout={timeout}")
            break

    del _mqtt_client
    return recv_msg


def show_device_config_modal(driver: webdriver.Chrome, device_card: WebElement, func_id: str) -> int:
    click_target = device_card.find_element(By.CSS_SELECTOR, '.settings_icon')
    js_click(driver, click_target)
    # validate
    try:
        driver.find_element(By.CSS_SELECTOR, '#device_config_modal_body')
    except:
        device_name = device_card.find_element(By.CSS_SELECTOR, '.dev_name').text
        elog(func_id, f"Device: {device_name}, Can not Open Config Modal")
        return 1

    return 0


def show_dimmer_modal(driver: webdriver.Chrome, device_card: WebElement, func_id: str) -> int:
    card_body = device_card.find_element(By.CSS_SELECTOR, '.dev_name')
    js_click(driver, card_body)
    # validate
    try:
        driver.find_element(By.CSS_SELECTOR, '#dimmer_modal_body')
    except:
        elog(func_id, 'Dimmer Control Modal Did not Open When Card Body Clicked')
        return 1

    return 0


def http_get_api_url():
    return f"http://{SERVER_IP}:{HTTP_PORT}/api"


def http_gen_at(username: str, password: str, role: str = 'ADMIN') -> str:
    server_url = http_get_api_url()
    api_url = f"{server_url}/login"
    json_req_body = {
        'username': username,
        'role': role,
        'password': password,
    }
    http_res = requests.post(api_url, json=json_req_body)
    json_res_body = json.loads(http_res.content.decode())
    return json_res_body['data']['access_token']


def http_get_device_info(func_id: str, device_name: str) -> dict | None:
    api_url = f"{http_get_api_url()}/get-device-info"

    try:
        admin_access_token = http_gen_at('test_admin', 'A9z2YyL2rVPivGSVkFpKitzfhSCDg6bN')
    except Exception as e:
        elog(func_id, f"Error in [http_gen_at] {e}")
        return None

    http_headers = {'Authorization': f"Bearer {admin_access_token}"}
    http_res = requests.post(api_url, headers=http_headers, json={'device_name': device_name})
    http_res_str = http_res.content.decode()
    json_res_body = json.loads(http_res_str)
    if not json_res_body['success']:
        elog(func_id, f"json_res_body={http_res_str}")
        return None

    return json_res_body['data']['device']
