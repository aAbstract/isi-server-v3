from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By


_MODULE_ID = 'e2e.us_room_search'


def us_room_search(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_room_search"
    reset_app(driver)
    exec_login_routine(driver)

    # exec routine [valid search seed]
    room_search_tf = driver.find_element(By.CSS_SELECTOR, '#rooms_search_tf')
    search_btn = driver.find_element(By.CSS_SELECTOR, '#search_btn')
    search_seed = 'Living Room'
    room_search_tf.send_keys(search_seed)
    js_click(driver, search_btn)
    # validate
    room_cards = driver.find_elements(By.CSS_SELECTOR, '.mobile_rooms_card_grid_sec')
    # check cards count
    if len(room_cards) != 1:
        elog(func_id, 'Seed did not filter grid results')
        return 1
    if room_cards[0].text != search_seed:
        elog(func_id, 'Seed returned mismatched result')
        return 1

    # exec routine [invalid search seed]
    room_search_tf.send_keys('Invalid Room')
    js_click(driver, search_btn)
    # validate
    err_span = driver.find_element(By.CSS_SELECTOR, '#mobile_rooms_err_msg')
    if err_span.text != 'Room Not Found':
        elog(func_id, 'Invalid Rooms search error msg on invalid input')
        return 1

    return 0
