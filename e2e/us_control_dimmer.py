from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By


_MODULE_ID = 'e2e.us_control_dimmer'
_CHECK_MODE = CHECK_MODE
REAL_EXP_STATE_MAP = {
    'ON': 'OFF',
    'OFF': 'ON',
}  # OLD:NEW


def _trigger_inten_action(driver: webdriver.Chrome, device_card: WebElement, inten_btn_fa_class: str, func_id: str) -> int:
    device_name = device_card.find_element(By.CSS_SELECTOR, '.dev_name').text
    state_target = device_card.find_element(By.CSS_SELECTOR, '.dev_state')
    inten_index_exp_val_map = {
        'fa-0': 0,
        'fa-1': 35,
        'fa-2': 70,
        'fa-3': 100,
    }

    def check_slider_state(val_to_check: int) -> int:
        status_text = try_get_elem_txt(driver, '#dimmer_status_text')
        if status_text == None:
            elog(func_id, 'Can not Read Slider Value [ELEM-TXT-TIMEOUT]')
            return 1

        status_val = int(status_text.split(': ')[1])
        if status_val != val_to_check:
            elog(func_id, 'Dimmer Control Modal Invalid Slider Value')
            return 1

        return 0

    # inten trigger
    inten_btn = driver.find_element(By.CSS_SELECTOR, f".dimmer_auto_control:has(.{inten_btn_fa_class})")
    js_click(driver, inten_btn)
    exp_state_val = inten_index_exp_val_map[inten_btn_fa_class]
    # UI validation
    rc = check_slider_state(exp_state_val)
    if rc != 0:
        return rc
    for fa_class in inten_index_exp_val_map.keys():
        css_classes = driver.find_element(By.CSS_SELECTOR, f".dimmer_auto_control:has(.{fa_class})").get_attribute('class')
        exp_css_classes = 'dimmer_auto_control dimmer_auto_control_active' if fa_class == inten_btn_fa_class else 'dimmer_auto_control'
        if css_classes != exp_css_classes:
            elog(func_id, f"Invalid Button Style, Style: {css_classes}, Expcted: {exp_css_classes}")
            return 1

    # REAL validation
    exp_state = 'LOADING' if _CHECK_MODE == 'IDLE' else str(exp_state_val)
    if state_target.text != exp_state:
        elog(func_id, f"Device: {device_name}, Action: {inten_btn_fa_class}, State: {state_target.text}, Expected: {exp_state}")
        return 1

    return 0


def us_control_dimmer_power_btn(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_dimmer_power_btn"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # compute expected state
    device_card = device_cards[DIMMER_DEVICE_INDEX]
    state_target = device_card.find_element(By.CSS_SELECTOR, '.dev_state')
    device_old_state = None
    exp_state = None
    if _CHECK_MODE == 'IDLE':
        exp_state = 'LOADING'
    elif _CHECK_MODE == 'REAL':
        device_old_state = state_target.text
        exp_state = REAL_EXP_STATE_MAP.get(device_old_state, 'OFF')

    # trigger action
    click_target = device_card.find_element(By.CSS_SELECTOR, '.power_icon')
    device_name = device_card.find_element(By.CSS_SELECTOR, '.dev_name').text
    js_click(driver, click_target)
    # validate
    if state_target.text != exp_state:
        elog(func_id, f"Device: {device_name}, State: {state_target.text}, Expected: {exp_state}")
        return 1

    return 0


def us_control_dimmer_modal_show(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_dimmer_modal_show"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    # open dimmer control modal
    rc = show_dimmer_modal(driver, device_cards[DIMMER_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc

    return 0


def us_control_dimmer_modal_inten_1(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_dimmer_modal_inten_1"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    rc = show_dimmer_modal(driver, device_cards[DIMMER_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc

    rc = _trigger_inten_action(driver, device_cards[DIMMER_DEVICE_INDEX], 'fa-1', func_id)
    if rc != 0:
        return rc
    return 0


def us_control_dimmer_modal_inten_2(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_dimmer_modal_inten_2"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    rc = show_dimmer_modal(driver, device_cards[DIMMER_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc

    rc = _trigger_inten_action(driver, device_cards[DIMMER_DEVICE_INDEX], 'fa-2', func_id)
    if rc != 0:
        return rc
    return 0


def us_control_dimmer_modal_inten_3(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_dimmer_modal_inten_3"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    rc = show_dimmer_modal(driver, device_cards[DIMMER_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc

    rc = _trigger_inten_action(driver, device_cards[DIMMER_DEVICE_INDEX], 'fa-3', func_id)
    if rc != 0:
        return rc
    return 0


def us_control_dimmer_modal_inten_0(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_control_dimmer_modal_inten_0"
    reset_app(driver)
    exec_login_routine(driver)
    device_cards = load_room_devices(driver, TESTING_ROOM_NAME, func_id)
    if not device_cards:
        return 1

    rc = show_dimmer_modal(driver, device_cards[DIMMER_DEVICE_INDEX], func_id)
    if rc != 0:
        return rc

    # force intensity to 70
    inten_2_btn = driver.find_element(By.CSS_SELECTOR, f".dimmer_auto_control:has(.fa-2)")
    js_click(driver, inten_2_btn)

    rc = _trigger_inten_action(driver, device_cards[DIMMER_DEVICE_INDEX], 'fa-0', func_id)
    if rc != 0:
        return rc
    return 0
