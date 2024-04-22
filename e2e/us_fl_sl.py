from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


_MODULE_ID = 'e2e.us_fl_sl'


def us_flood_sensor_notif(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_flood_sensor_notif"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # check flood sensor link is suspended
    device_card = device_cards[FL_DEVICE_INDEX]
    try:
        conn_state_icon = device_card.find_element(By.CSS_SELECTOR, '.fa-link')
        css_classes = conn_state_icon.get_attribute('class')
        if 'dev_suspend_icon' not in css_classes:
            elog(func_id, 'Flood Sensor Device Card Connection State is not Suspended')
            return 1
    except:
        elog(func_id, 'Flood Sensor Device Card Does not Have a fa-link Element')
        return 1

    # trigger flood sensor notif
    publish_mqtt_msg(f"telem/{FL_DEVICE_NAME}/notif", 'FLOOD')
    # validate
    notif_header = try_get_elem_txt(driver, '.center_notif .p-toast-message .p-toast-message-text .p-toast-summary')
    if notif_header == None:
        elog(func_id, 'Can not Get Notif Header [ELEM-TXT-TIMEOUT]')
        return 1
    exp_val = f"Room:living_room_0 Device:{FL_DEVICE_NAME}"
    if notif_header != exp_val:
        elog(func_id, f"Invalid Notif Header, notif_header: {notif_header}, Expected: {exp_val}")
        return 1

    notif_body = try_get_elem_txt(driver, '.center_notif .p-toast-message .p-toast-message-text .p-toast-detail')
    if notif_body == None:
        elog(func_id, 'Can not Get Notif Body [ELEM-TXT-TIMEOUT]')
        return 1
    exp_val = 'Flood Detected'
    if notif_body != exp_val:
        elog(func_id, f"Invalid Notif Body, notif_body: {notif_body}, Expected: {exp_val}")
        return 1

    # close notif
    close_btn = driver.find_element(By.CSS_SELECTOR, '.center_notif .p-toast-icon-close')
    js_click(driver, close_btn)

    return 0


def us_sec_lock_notif(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_sec_lock_notif"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # check security lock link is suspended
    device_card = device_cards[SL_DEVICE_INDEX]
    try:
        conn_state_icon = device_card.find_element(By.CSS_SELECTOR, '.fa-link')
        css_classes = conn_state_icon.get_attribute('class')
        if 'dev_suspend_icon' not in css_classes:
            elog(func_id, 'Security Lock Device Card Connection State is not Suspended')
            return 1
    except:
        elog(func_id, 'Security Lock Device Card Does not Have a fa-link Element')
        return 1

    # trigger flood sensor notif
    publish_mqtt_msg(f"telem/{SL_DEVICE_NAME}/notif", 'UNLOCKED')
    # validate
    notif_header = try_get_elem_txt(driver, '.center_notif .p-toast-message .p-toast-message-text .p-toast-summary')
    if notif_header == None:
        elog(func_id, 'Can not Get Notif Header [ELEM-TXT-TIMEOUT]')
        return 1
    exp_val = f"Room:living_room_0 Device:{SL_DEVICE_NAME}"
    if notif_header != exp_val:
        elog(func_id, f"Invalid Notif Header, notif_header: {notif_header}, Expected: {exp_val}")
        return 1

    notif_body = try_get_elem_txt(driver, '.center_notif .p-toast-message .p-toast-message-text .p-toast-detail')
    if notif_body == None:
        elog(func_id, 'Can not Get Notif Body [ELEM-TXT-TIMEOUT]')
        return 1
    exp_val = 'Lock Opened'
    if notif_body != exp_val:
        elog(func_id, f"Invalid Notif Body, notif_body: {notif_body}, Expected: {exp_val}")
        return 1

    # close notif
    close_btn = driver.find_element(By.CSS_SELECTOR, '.center_notif .p-toast-icon-close')
    js_click(driver, close_btn)

    return 0
