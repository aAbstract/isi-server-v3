import time
from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


_MODULE_ID = 'e2e.us_control_motion'
_CHECK_MODE = CHECK_MODE
REAL_EXP_STATE_MAP = {
    'ON': 'OFF',
    'OFF': 'ON',
}  # OLD:NEW


def _force_device_config(func_id: str, driver: webdriver.Chrome, device_card: WebElement, sec_mode: int, light_mode: int) -> int:
    rconfig_map = {
        1: 'Enable',
        0: 'Disable',
    }
    rc = show_device_config_modal(driver, device_card, func_id)
    if rc != 0:
        return rc
    sec_mode_select, light_mode_select = driver.find_elements(By.CSS_SELECTOR, '.config_control_cont .p-dropdown')

    js_click(driver, sec_mode_select)
    target_op = driver.find_element(By.CSS_SELECTOR, f'.p-dropdown-item[aria-label="{rconfig_map[sec_mode]}"]')
    js_click(driver, target_op)
    time.sleep(ANIMATION_DELAY)
    close_btn = driver.find_element(By.CSS_SELECTOR, '.p-toast-icon-close')
    js_click(driver, close_btn)

    time.sleep(ANIMATION_DELAY)

    js_click(driver, light_mode_select)
    target_op = driver.find_element(By.CSS_SELECTOR, f'.p-dropdown-item[aria-label="{rconfig_map[light_mode]}"]')
    js_click(driver, target_op)
    time.sleep(ANIMATION_DELAY)
    close_btn = driver.find_element(By.CSS_SELECTOR, '.p-toast-icon-close')
    js_click(driver, close_btn)

    return 0


def us_control_motion_card_body(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_motion_card_body"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[MOTION_DEVICE_INDEX]
    state_target = device_card.find_element(By.CSS_SELECTOR, '.dev_state')
    device_old_state = None
    exp_state = None
    if _CHECK_MODE == 'IDLE':
        exp_state = 'LOADING'
    elif _CHECK_MODE == 'REAL':
        device_old_state = state_target.text
        exp_state = REAL_EXP_STATE_MAP[device_old_state]

    # trigger action
    click_target = device_card.find_element(By.CSS_SELECTOR, '.dev_name')
    device_name = click_target.text
    js_click(driver, click_target)
    # validate
    if state_target.text != exp_state:
        elog(func_id, f"Device: {device_name}, State: {state_target.text}, Expected: {exp_state}")
        return 1

    return 0


def us_control_motion_card_power_btn(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_motion_card_power_btn"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[MOTION_DEVICE_INDEX]
    state_target = device_card.find_element(By.CSS_SELECTOR, '.dev_state')
    device_old_state = None
    exp_state = None
    if _CHECK_MODE == 'IDLE':
        exp_state = 'LOADING'
    elif _CHECK_MODE == 'REAL':
        device_old_state = state_target.text
        exp_state = REAL_EXP_STATE_MAP[device_old_state]

    # trigger action
    click_target = device_card.find_element(By.CSS_SELECTOR, '.power_icon')
    device_name = device_card.find_element(By.CSS_SELECTOR, '.dev_name').text
    js_click(driver, click_target)
    # validate
    if state_target.text != exp_state:
        elog(func_id, f"Device: {device_name}, State: {state_target.text}, Expected: {exp_state}")
        return 1

    return 0


def us_motion_config(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_motion_config"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    rc = show_device_config_modal(driver, device_cards[MOTION_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc

    def match_server_ui_config() -> tuple[int, dict]:
        device_info = http_get_device_info(func_id, MOTION_DEVICE_NAME)
        if device_info == None:
            return 1, None

        config_map = {
            'Disable': 0,
            'Enable': 1,
        }

        server_config: dict = device_info['config']
        ui_config_vals = try_get_elem_txts(driver, '.config_control_cont .p-dropdown')
        ui_config = {
            'sec_mode': config_map.get(ui_config_vals[0], 'UNKNOWN'),
            'light_mode': config_map.get(ui_config_vals[1], 'UNKNOWN'),
        }
        if server_config != ui_config:
            elog(func_id, f"server_config!=ui_config, server_config={server_config}, ui_config={ui_config}")
            return 1, None

        return 0, server_config

    # check server and ui config match
    rc, old_config = match_server_ui_config()
    if rc != 0:
        return rc

    def inv_select(sel_elem: WebElement, current_val: int):
        iconfig_map = {
            0: 'Enable',
            1: 'Disable',
        }
        js_click(driver, sel_elem)
        target_op = driver.find_element(By.CSS_SELECTOR, f'.p-dropdown-item[aria-label="{iconfig_map[current_val]}"]')
        js_click(driver, target_op)
        # close notif
        time.sleep(ANIMATION_DELAY)
        close_btn = driver.find_element(By.CSS_SELECTOR, '.p-toast-icon-close')
        js_click(driver, close_btn)

    # change config from ui
    sec_mode_select, light_mode_select = driver.find_elements(By.CSS_SELECTOR, '.config_control_cont .p-dropdown')
    inv_select(sec_mode_select, old_config['sec_mode'])
    time.sleep(ANIMATION_DELAY)
    inv_select(light_mode_select, old_config['light_mode'])

    # check old and new config match
    rc, new_config = match_server_ui_config()
    if rc != 0:
        return rc

    def inv_val(x) -> int | None:
        out_map = {
            0: 1,
            1: 0,
        }
        return out_map.get(x, None)
    inv_old_config = {
        'sec_mode': inv_val(old_config['sec_mode']),
        'light_mode': inv_val(old_config['light_mode']),
    }
    if new_config != inv_old_config:
        elog(func_id, f"new_config!=inv_old_config, new_config={new_config}, inv_old_config={inv_old_config}")
        return 1

    return 0


def us_motion_sensor_sec_mode(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_motion_sensor_sec_mode"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # configure motion sensor
    rc = show_device_config_modal(driver, device_cards[MOTION_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc
    rc = _force_device_config(func_id, driver, device_cards[MOTION_DEVICE_INDEX], 1, 0)
    if rc != 0:
        return rc

    # trigger automation
    publish_mqtt_msg(f"telem/{MOTION_DEVICE_NAME}/notif", 'MOTION')
    time.sleep(MQTT_DELAY)

    # validate
    notif_header = try_get_elem_txt(driver, '.center_notif .p-toast-message .p-toast-message-text .p-toast-summary')
    if notif_header == None:
        elog(func_id, 'Can not Get Notif Header [ELEM-TXT-TIMEOUT]')
        return 1
    exp_val = f"Room:living_room_0 Device:{MOTION_DEVICE_NAME}"
    if notif_header != exp_val:
        elog(func_id, f"Invalid Notif Header, notif_header: {notif_header}, Expected: {exp_val}")
        return 1

    notif_body = try_get_elem_txt(driver, '.center_notif .p-toast-message .p-toast-message-text .p-toast-detail')
    if notif_body == None:
        elog(func_id, 'Can not Get Notif Body [ELEM-TXT-TIMEOUT]')
        return 1
    exp_val = 'Motion Detected'
    if notif_body != exp_val:
        elog(func_id, f"Invalid Notif Body, notif_body: {notif_body}, Expected: {exp_val}")
        return 1

    # close notif
    close_btn = driver.find_element(By.CSS_SELECTOR, '.center_notif .p-toast-icon-close')
    js_click(driver, close_btn)

    return 0


def us_motion_sensor_light_mode(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_motion_sensor_light_mode"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # configure motion sensor
    rc = show_device_config_modal(driver, device_cards[MOTION_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc
    rc = _force_device_config(func_id, driver, device_cards[MOTION_DEVICE_INDEX], 0, 1)
    if rc != 0:
        return rc

    # trigger automation
    publish_mqtt_msg(f"telem/{MOTION_DEVICE_NAME}/notif", 'MOTION')

    # validate
    mqtt_msg = read_mqtt_msg(func_id, 'command/main_switch_0/power_1')
    if mqtt_msg != 'ON':
        elog(func_id, f"Invalid Read MQTT Msg, Msg: {mqtt_msg}, Expected: ON")
        return 1

    return 0
