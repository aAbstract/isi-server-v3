import time
import json
from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By


_MODULE_ID = 'e2e.us_scenes'


def _show_scene_modal(driver: webdriver.Chrome, func_id: str) -> int:
    click_target = driver.find_element(By.CSS_SELECTOR, '#create_scene_btn_cont button')
    js_click(driver, click_target)
    # validate
    try:
        driver.find_element(By.CSS_SELECTOR, '#scene_modal_body')
    except:
        elog(func_id, 'Can not Open Smart Scene Modal')
        return 1

    return 0


def us_trigger_scene(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_trigger_scene"
    reset_app(driver)
    exec_login_routine(driver)
    bottom_bar_click(driver, 'Scenes')

    # load scenes cards
    scenes_cards = driver.find_elements(By.CSS_SELECTOR, '.smart_scene_card')
    if len(scenes_cards) == 0:
        elog(func_id, 'System Does not Have any Smart Scenes')
        return 1

    # trigger a scene
    js_click(driver, scenes_cards[0])

    # validate
    mqtt_msg = read_mqtt_msg(func_id, 'telem/client/notif')
    msg_obj = json.loads(mqtt_msg)
    exp_msg_obj = {'msg_lvl': 'info', 'msg_body': 'Scene Executed: Home Entrance'}
    if msg_obj != exp_msg_obj:
        elog(func_id, f"MQTT Notif Msg Mismatch, Msg: {msg_obj}, Expected: {exp_msg_obj}")
        return 1

    return 0


def us_create_scene(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_create_scene"
    reset_app(driver)
    exec_login_routine(driver)
    bottom_bar_click(driver, 'Scenes')

    # load scenes cards
    scenes_cards = driver.find_elements(By.CSS_SELECTOR, '.smart_scene_card')
    if len(scenes_cards) == 0:
        elog(func_id, 'System Does not Have any Smart Scenes')
        return 1

    rc = _show_scene_modal(driver, func_id)
    if rc != 0:
        return rc

    # input scene name
    smart_scene_name = 'E2E Test Scene'
    scene_name_tf = driver.find_element(By.CSS_SELECTOR, '#scene_name_tf')
    scene_name_tf.send_keys(smart_scene_name)

    # click record actions
    click_target = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Record Actions"]')
    js_click(driver, click_target)
    # validate
    status_bar_txt = try_get_elem_txt(driver, '#status_bar_txt')
    exp_status_bar_txt = 'Recording Control Actions [Click To Stop]'
    if status_bar_txt != exp_status_bar_txt:
        elog(func_id, f"Status Bar Text Mismatch, status_bar_txt={status_bar_txt}, exp_status_bar_txt={exp_status_bar_txt}")
        return 1

    # capture actions
    actions_list = []
    bottom_bar_click(driver, 'Home')
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1
    # switch action
    switch_device_card = device_cards[SWITCH_DEVICE_INDEX]
    click_target = switch_device_card.find_element(By.CSS_SELECTOR, '.power_icon')
    js_click(driver, click_target)
    # validate
    status_bar_txt = try_get_elem_txt(driver, '#status_bar_txt')
    exp_status_bar_txt = f"Recorded: {SWITCH_DEVICE_NAME}-TOGGLE"
    if status_bar_txt != exp_status_bar_txt:
        elog(func_id, f"Status Bar Text Mismatch, status_bar_txt={status_bar_txt}, exp_status_bar_txt={exp_status_bar_txt}")
        return 1
    actions_list.append(status_bar_txt.replace('Recorded: ', ''))
    # dimmer action
    rc = show_dimmer_modal(driver, device_cards[DIMMER_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc
    inten_btn = driver.find_element(By.CSS_SELECTOR, '.dimmer_auto_control:has(.fa-1)')
    js_click(driver, inten_btn)
    # validate
    status_bar_txt = try_get_elem_txt(driver, '#status_bar_txt')
    exp_status_bar_txt = f"Recorded: {DIMMER_DEVICE_NAME}-DIM_1"
    if status_bar_txt != exp_status_bar_txt:
        elog(func_id, f"Status Bar Text Mismatch, status_bar_txt={status_bar_txt}, exp_status_bar_txt={exp_status_bar_txt}")
        return 1
    actions_list.append(status_bar_txt.replace('Recorded: ', ''))

    # stop actions recording
    click_target = driver.find_element(By.CSS_SELECTOR, '#status_bar_txt')
    js_click(driver, click_target)
    # validate modal reopen
    try:
        driver.find_element(By.CSS_SELECTOR, '#scene_modal_body')
    except:
        elog(func_id, 'Smart Scene Modal Did not Reopen')
        return 1
    # validate actions list
    ui_actions_list = try_get_elem_txts(driver, '.p-listbox-item')
    if actions_list != ui_actions_list:
        elog(func_id, f"Actions List Mismatch, ui_actions_list={ui_actions_list}, actions_list={actions_list}")
        return 1

    # send create scene request
    click_target = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Create"]')
    js_click(driver, click_target)
    time.sleep(HTTP_DELAY)
    # validate
    new_smart_scenes = try_get_elem_txts(driver, '.scene_card_name')
    if smart_scene_name not in new_smart_scenes:
        elog(func_id, f"Smart Scene [{smart_scene_name}] Did not Show in Smart Scenes List [{new_smart_scenes}]")
        return 1

    # delete created scene
    last_scene_card = driver.find_elements(By.CSS_SELECTOR, '.smart_scene_card')[-1]
    click_target = last_scene_card.find_element(By.CSS_SELECTOR, '.ai_del')
    js_click(driver, click_target)
    time.sleep(HTTP_DELAY)
    # validate
    new_smart_scenes = try_get_elem_txts(driver, '.scene_card_name')
    if smart_scene_name in new_smart_scenes:
        elog(func_id, f"Smart Scene [{smart_scene_name}] is not Deleted, new_smart_scenes={new_smart_scenes}")
        return 1

    return 0
