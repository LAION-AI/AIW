# Description: This file contains the functions to obtain the cookies from the chat.lmsys.org website.
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import json

def get_selenium_webdriver_firefox():
    """
    Get a selenium webdriver with Firefox.
    Returns:
        (webdriver.Firefox): A selenium webdriver.
    """

    options = Options()
    options.headless = False
    driver = webdriver.Firefox(options=options)
    return driver

def obtain_cookies(file_path='cookies.json'):
    """
    Obtain the cookies from the chat.lmsys.org website.
    Args:
        file_path (str): The path to save the cookies.
    Returns:
        (str): The user agent.
    """

    url = 'https://chat.lmsys.org/'

    driver = get_selenium_webdriver_firefox()
    driver.get(url)
    time.sleep(30)
    cookies = driver.get_cookies()
    user_agent = driver.execute_script("return navigator.userAgent")


    cookies = {cookie['name']: cookie['value'] for cookie in cookies}

    with open(file_path, 'w') as f:
        json.dump(cookies, f)

    driver.close()
    return user_agent