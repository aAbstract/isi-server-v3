from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


_MODULE_ID = 'e2e.us_view_temp_humd'
REAL_EXP_STATE_MAP = {
    'ON': 'OFF',
    'OFF': 'ON',
}  # OLD:NEW


def us_control_temp_device(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_temp_device"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    device_card = device_cards[TEMP_DEVICE_INDEX]
    device_state = device_card.find_element(By.CSS_SELECTOR, '.dev_state').text
    if device_state == 'NONE':
        elog(func_id, f"Temperate Device State is NONE. Make Sure Device [{TEMP_DEVICE_NAME}] is Online")
        return 1

    # create valid inital state
    if device_state == 'ON':
        click_target = device_card.find_element(By.CSS_SELECTOR, '.power_icon')
        js_click(driver, click_target)
    # validate
    while True:
        device_state = device_card.find_element(By.CSS_SELECTOR, '.dev_state').text
        if device_state != 'LOADING':
            break
    if device_state != 'OFF':
        elog(func_id, f"Device: {TEMP_DEVICE_NAME}, Invalid Initial Device State: {device_state}")
        return 1

    # trigger action
    click_target = device_card.find_element(By.CSS_SELECTOR, '.power_icon')
    js_click(driver, click_target)
    # validate
    while True:
        device_state = device_card.find_element(By.CSS_SELECTOR, '.dev_state').text
        if device_state == 'LOADING':
            continue
        try:
            break
        except:
            elog(func_id, f"Device: {TEMP_DEVICE_NAME}, Can not Parse Device State: {device_state}")
            return 1

    return 0


def us_control_humd_device(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_humd_device"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    device_card = device_cards[HUMD_DEVICE_INDEX]
    device_state = device_card.find_element(By.CSS_SELECTOR, '.dev_state').text
    if device_state == 'NONE':
        elog(func_id, f"Humidity Device State is NONE. Make Sure Device [{HUMD_DEVICE_NAME}] is Online")
        return 1

    # create valid inital state
    if device_state == 'ON':
        click_target = device_card.find_element(By.CSS_SELECTOR, '.power_icon')
        js_click(driver, click_target)
    # validate
    while True:
        device_state = device_card.find_element(By.CSS_SELECTOR, '.dev_state').text
        if device_state != 'LOADING':
            break
    if device_state != 'OFF':
        elog(func_id, f"Device: {HUMD_DEVICE_NAME}, Invalid Initial Device State: {device_state}")
        return 1

    # trigger action
    click_target = device_card.find_element(By.CSS_SELECTOR, '.power_icon')
    js_click(driver, click_target)
    # validate
    while True:
        device_state = device_card.find_element(By.CSS_SELECTOR, '.dev_state').text
        if device_state == 'LOADING':
            continue
        try:
            break
        except:
            elog(func_id, f"Device: {HUMD_DEVICE_NAME}, Can not Parse Device State: {device_state}")
            return 1

    return 0
