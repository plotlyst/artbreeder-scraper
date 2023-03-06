import json
import time

from atomicwrites import atomic_write
from selenium import webdriver

# driver = webdriver.Chrome(executable_path='/home/zkovari/Downloads/chromedriver')
driver = webdriver.Chrome()
driver.get("https://www.artbreeder.com/browse?sort=trending&modelName=portraits_sg2")

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

i = 0
while i < 25:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    i += 1

urls = []
elements = driver.find_elements('xpath', "//*[@alt='img from artbreeder']")
for el in elements:
    img_src = el.get_attribute('src')
    if img_src:
        urls.append(img_src)

driver.close()

with atomic_write('resources/artbreeder/portraits.json', overwrite=True) as f:
    f.write(json.dumps(urls))
