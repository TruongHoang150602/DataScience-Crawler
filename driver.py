from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from utils import wait_and_click, wait_for_element
import os
import time

def configure_webdriver(url):
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-web-security')
   
    service = Service(executable_path=ChromeDriverManager().install())
    # capabilities = options.to_capabilities()
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url=url)
    return driver


