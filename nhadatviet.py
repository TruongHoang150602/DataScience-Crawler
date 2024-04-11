from selenium.webdriver.common.by import By
import pymongo
from driver import configure_webdriver
from utils import wait_for_element, wait_for_elements, wait_and_get_for_element, wait_until_page_loads
import time
from seleniumwire.utils import decode
import json

def get_link_post(driver):
    list_url = []
    
    for page in range(1,100):
        url = f"https://123nhadatviet.com/rao-vat/can-ban/nha-dat/t1/ha-noi/trang--{page}.html"
        print(f"page: {page}")
        driver.get(url)
        wait_until_page_loads(driver, timeout=2)
        try:
            titles = wait_for_elements(driver, (By.CLASS_NAME, "ct_title"))
            for title in titles:
                link = title.find_element(By.CSS_SELECTOR, "a").get_attribute("href") 
                list_url.append(link)
        except Exception as e:
            print(f"Error: {page}")
            print(e)
            time.sleep(30) #nhap capcha
            break
    
    # Save list_url to a file
    with open('nhadatviet.txt', 'w') as f:
        for url in list_url:
            f.write(url + '\n')

def get_detail_data(driver, url, collection):
    driver.get(url)
    wait_until_page_loads(driver, timeout=3)

    data = {}
    try:
        data["title"] = wait_and_get_for_element(driver, (By.TAG_NAME, "h1"))
        basic_info_rows = wait_for_elements(driver, (By.CSS_SELECTOR, ".moreinfor1 .infor tr"))
        for row in basic_info_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for i in range(0, len(cells), 2):
                key = cells[i].text.strip()
                value = cells[i + 1].text.strip()
                data[key] = value

        data["description"] = wait_and_get_for_element(driver, (By.CSS_SELECTOR, ".detail.text-content"))
        data["contact_name"] = wait_and_get_for_element(driver, (By.CSS_SELECTOR, (".contact-info .name")))
        data["contact_phone"] = wait_and_get_for_element(driver, (By.CSS_SELECTOR, (".contact-info .fone")))
        address_value = wait_and_get_for_element(driver, (By.CSS_SELECTOR, (".address .value")))

        components = address_value.split(", ")
        street = components[0].split(" ")[1:]  # Remove the first element which is not part of the street
        street = " ".join(street)
        ward = components[1].split(" ")[1:]
        ward = " ".join(ward)
        district = components[2].split(" ")[1:]
        district = " ".join(district)
        province = components[3]

        data['address'] = {
            "street": street,
            "ward": ward,
            "district": district,
            "province": province
        }

    except:
        print(f"Error: {url}")
        time.sleep(30)
        return
    collection.insert_one(data)


if __name__ == "__main__":
    driver = configure_webdriver("https://123nhadatviet.com/")
    time.sleep(2)
    # get_link_post(driver)

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["DataScience"]
    collection = db["nhadatviet"]

    # Open the file in read mode
    with open('nhadatviet.txt', 'r') as file:
        # Read each line and store them into a list
        url_list = file.readlines()
    # Strip newline characters from each URL
    url_list = [url.strip() for url in url_list]
    for url in url_list:
        get_detail_data(driver, url, collection)

    driver.quit()
