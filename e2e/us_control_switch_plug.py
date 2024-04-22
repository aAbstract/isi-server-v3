from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


_MODULE_ID = 'e2e.us_control_switch_plug'
_CHECK_MODE = CHECK_MODE
REAL_EXP_STATE_MAP = {
    'ON': 'OFF',
    'OFF': 'ON',
}  # OLD:NEW


def us_control_switch_card_body(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_switch_card_body"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[SWITCH_DEVICE_INDEX]
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


def us_control_switch_card_power_btn(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_switch_card_power_btn"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[SWITCH_DEVICE_INDEX]
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


def us_control_plug_card_body(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_plug_card_body"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[PLUG_DEVICE_INDEX]
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


def us_control_plug_card_power_btn(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_plug_card_power_btn"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[PLUG_DEVICE_INDEX]
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
