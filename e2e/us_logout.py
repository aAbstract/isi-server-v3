from e2e_utils import *
from us_login import exec_login_routine
from selenium import webdriver
from selenium.webdriver.common.by import By

_MODULE_ID = 'e2e.us_logout'


def us_logout(driver: webdriver.Chrome):
    func_id = f"{_MODULE_ID}.us_logout"
    reset_app(driver)
    exec_login_routine(driver)
    bottom_bar_click(driver, 'Logout')
    login_txt = try_get_elem_txt(driver, '#login_span_indic')
    exp_login_txt = 'Login to Continue'
    if login_txt != exp_login_txt:
        elog(func_id, f"Login Text Mismatch, Text: {login_txt}, Expected: {exp_login_txt}")
        return 1

    return 0
