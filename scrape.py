import json
import re
import time

from atomicwrites import atomic_write
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.artbreeder.com/browse?sort=trending&modelName=portraits_sg2")
# elem = driver.find_element('xpath', "//*[@data-name='portraits_sg2']")
# elem.click()

SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

i = 0
while i < 50:
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
elements = driver.find_elements('class name', 'main_image')
for el in elements:
    match = re.search(r'http.*\.(jpeg|png|jpg|gif)', el.get_attribute('style'))
    if match:
        urls.append(match.group(0))

driver.close()

with atomic_write('resources/artbreeder/portraits.json', overwrite=True) as f:
    f.write(json.dumps(urls))
