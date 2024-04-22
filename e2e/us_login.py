from e2e_utils import *
from selenium import webdriver
from selenium.webdriver.common.by import By


_MODULE_ID = 'e2e.us_login'


def exec_login_routine(driver: webdriver.Chrome):
    # exec routine
    username_tf = driver.find_element(By.CSS_SELECTOR, '#username_tf')
    password_tf = driver.find_element(By.CSS_SELECTOR, '#password_tf')
    login_btn = driver.find_element(By.CSS_SELECTOR, '#login_btn')
    username_tf.send_keys('test_user')
    password_tf.send_keys('test_user_pass_123')
    js_click(driver, login_btn)


def us_login(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_login"
    reset_app(driver)
    exec_login_routine(driver)

    # validate
    room_name_header = driver.find_element(By.CSS_SELECTOR, '#room_name_header')
    if room_name_header.text != 'House Rooms':
        elog(func_id, '#room_name_header.text value mismatch')
        return 1

    return 0
