import os
import time
import json
import imghdr
import requests
import threading
import wget

from requests_html import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(chrome_options=chrome_options)


def get_image_url():
    """Returns search image url"""

    driver.maximize_window()

    driver.get("https://yandex.com/images/")

    time.sleep(8)

    search = driver.find_element(By.CSS_SELECTOR, "input[type='file']")

    image_folder_path = os.getcwd() + "/search-image/"
    image_name = os.listdir(image_folder_path)[0]
    file_type = imghdr.what(image_folder_path + image_name)
    if file_type in (".jpg", "jpeg", "png", "gif"):
        search.send_keys(os.getcwd() + f"/search-image/{image_name}")
    else:
        driver.quit()
        raise Exception("Image format not supported")

    time.sleep(10)

    # Navigate to the page with the "cbir_page=similar" query parameter
    url = driver.current_url + "&cbir_page=similar" + "&isize=large"

    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        return url
    else:
        return None


def get_data() -> dict:
    """Returns dict of image urls"""
    time.sleep(10)

    url_dict = {}

    a_herf = driver.find_element(
        By.CLASS_NAME,
        "serp-list.serp-list_type_search.serp-list_unique_yes.serp-list_rum_yes.serp-list_justifier_yes.serp-controller__list.counter__reqid.clearfix.i-bem.serp-list_js_inited",
    )

    div_list = a_herf.find_elements(By.TAG_NAME, "div")
    data_list = []
    for div in div_list:
        if div.get_attribute("data-bem") is not None:
            data_list.append(div.get_attribute("data-bem"))

    for data in data_list:
        json_data = json.loads(data)
        if "serp-item" in json_data:
            if "img_href" in json_data["serp-item"]:
                url_dict[json_data["serp-item"]["img_href"]] = json_data["serp-item"][
                    "img_href"
                ]

    print(f"Total image urls count:{len(url_dict)}")
    return url_dict


def scroll_down(page_size):
    """Scroll down to bottom of the page"""
    scroll_pause_time = 3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(page_size):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def save_image_requests(src):
    """Save image from url"""
    # open scrapped_images folder and save images
    if not os.path.exists("scrapped_images"):
        os.makedirs("scrapped_images")

    if not os.path.exists("failed_urls.txt"):
        with open("failed_urls.txt", "w") as file:
            pass

    try:
        # download images
        wget.download(src, os.getcwd() + "/scrapped_images/")
    except Exception as e:
        with open("failed_urls.txt", "a") as file:
            file.write(src + "\n")


def save_image(url_dict: dict):
    """Save image"""
    threads = []

    # Iterate through the dictionary and create a thread for each image
    for url in url_dict.values():
        t = threading.Thread(target=save_image_requests, args=(url,))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()
