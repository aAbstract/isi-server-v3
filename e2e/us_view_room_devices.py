from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


_MODULE_ID = 'e2e.us_view_room_devices'


def us_view_room_devices(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_view_room_devices"
    reset_app(driver)
    exec_login_routine(driver)

    # exec routine [room contains devices]
    room_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_rooms_card_grid_sec')
    living_room_card = [card for card in room_cards if card.text == 'Living Room'][0]
    js_click(driver, living_room_card)
    # validate
    device_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_room_card')
    if len(device_cards) == 0:
        elog(func_id, 'Can not display room devices')
        return 1

    # exec routine [room does not contain devices]
    bottom_bar_click(driver, 'Home')
    room_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_rooms_card_grid_sec')
    living_room_card = [card for card in room_cards if card.text == 'Home Gym'][0]
    js_click(driver, living_room_card)
    # validate
    status_text_h3 = driver.find_element(By.CSS_SELECTOR, '#mobile_room_status')
    if status_text_h3.text != 'No Devices Found in This Room':
        elog(func_id, '#mobile_room_status.text value mismatch')
        return 1

    # check device card structure
    bottom_bar_click(driver, 'Home')
    room_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_rooms_card_grid_sec')
    living_room_card = [card for card in room_cards if card.text == 'Living Room'][0]
    js_click(driver, living_room_card)
    device_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_room_card')
    device_cards_count = len(device_cards)

    # check device icons
    device_icon_svgs = driver.find_elements(By.CSS_SELECTOR, '.mobile_room_card .header .dev_icon')
    icons_count = len(device_icon_svgs)
    if icons_count != device_cards_count:
        elog(func_id, 'Device Cards Number not Equal to Device Icons Number')
        return 1

    # check device connection states
    offline_conn_state_icons = driver.find_elements(By.CSS_SELECTOR, '.dev_offline_icon')
    offline_count = len(offline_conn_state_icons)
    suspend_conn_state_icons = driver.find_elements(By.CSS_SELECTOR, '.dev_suspend_icon')
    suspend_count = len(suspend_conn_state_icons)
    online_conn_state_icons = driver.find_elements(By.CSS_SELECTOR, '.dev_online_icon')
    online_count = len(online_conn_state_icons)
    # validate
    if (offline_count + suspend_count + online_count) != device_cards_count:
        elog(func_id, 'Some Device Cards Do not Have Connection State')
        return 1

    # check device quick actions
    settings_quick_actions_btns = driver.find_elements(By.CSS_SELECTOR, '.settings_icon')
    settings_qabtn_count = len(settings_quick_actions_btns)
    # validate
    if settings_qabtn_count != device_cards_count:
        elog(func_id, 'Some Device Cards Do not Have Quick Action Buttons')
        return 1

    # check device names
    device_names = driver.find_elements(By.CSS_SELECTOR, '.dev_name')
    names_count = len(device_names)
    # validate
    if names_count != device_cards_count:
        elog(func_id, 'Some Device Cards Do not Have a Device Name')
        return 1

    # check device states
    devices_states = driver.find_elements(By.CSS_SELECTOR, '.dev_state')
    states_count = len(devices_states)
    # validate
    if states_count != device_cards_count:
        elog(func_id, 'Some Device Cards Do not Have a Device State')
        return 1

    # check hidden power button in suspend devices
    suspend_devices = driver.find_elements(By.CSS_SELECTOR, '.mobile_room_card:has(.dev_suspend_icon)')
    for sdev in suspend_devices:
        try:
            sdev.find_element(By.CSS_SELECTOR, '.power_icon')
            sdev_name = get_elem_txt(sdev, '.dev_name')
            if sdev_name == None:
                elog(func_id, 'Error Reading Device Card Name')
                return 1

            elog(func_id, f"Device [{sdev_name}] is Suspended but Has a Power Button")
            return 1
        except:
            pass

    # check sleep state in suspend devices
    for sdev in suspend_devices:
        sdev_name = get_elem_txt(sdev, '.dev_name')
        if sdev_name == None:
            elog(func_id, 'Error Reading Device Card Name')
            return 1

        sdev_state = get_elem_txt(sdev, '.dev_state')
        if sdev_state == None:
            elog(func_id, f"Error Reading Device [{sdev_name}] State")
            return 1

        if sdev_state != 'SLEEP':
            elog(func_id, f"Device [{sdev_name}] is Suspended but State is not SLEEP")
            return 1

    return 0
