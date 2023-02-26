import time, io
import random
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from ..model import infer

def get_random_candidates() -> list[str]:
    xpaths = []
    for i in range(161, 177+1):
        xpaths.append(f'//input[@value="{i}"]')
    random.shuffle(xpaths)
    xpaths = xpaths[:9]
    xpaths.append('//input[@value="179"]')
    return xpaths

def start():
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    for _ in range(100):
        driver.get("http://tainangtrevietnam.vn/index.html")

        captcha_image = driver.find_element(by = By.XPATH,
            value = r'//*[@id="thongtin"]/div/div[3]/div[2]/div/img')

        result = infer.inference(captcha_image.screenshot_as_png)

        text_box = driver.find_element(by = By.XPATH,
            value = r'//input[@class="inputVote"]')
        text_box.send_keys(result)

        for xpath in get_random_candidates():
            check_box = driver.find_element(by = By.XPATH, value = xpath)
            check_box.click()

        time.sleep(10)

        submit_button = driver.find_element(by = By.XPATH,
            value = r'//*[@id="ctl00_webPartManager_wp793523384_wp1892398315_btnSubmit1"]')
        submit_button.click()
        
        alert = driver.switch_to.alert
        print(f"Result: {alert.text}")
        alert.accept()
