import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from seleniumwire.utils import decode
import json

def wait_and_click(driver, locator, timeout=30):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
    element.click()

def wait_for_element(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))

def wait_and_get_for_element(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator)).text.strip()

def wait_for_elements(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))

def wait_until_page_loads(driver, timeout=30):
    time.sleep(timeout)  # For simplicity, we just use time.sleep to wait for the page to load

def extract_uid_from_link(link):
    href = link.get_attribute("href")
    return href.split("/")[-1]

