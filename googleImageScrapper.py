#! python3
# googleImageScrapper.py - Downloads images from google image.
# Created at Sep, 16 2020

import pyinputplus as pyip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import requests
import time

baseUrl = 'https://www.google.com/search?tbm=isch&q='

# Get user input for keyword
keyword = pyip.inputStr('Enter a keyword : ')

# Opening the web
browser = webdriver.Chrome()
browser.get(baseUrl + keyword)

# Pressing End key as long as we haven't reach the bottom page yet
while True:
    show_more_button = browser.find_element_by_css_selector(
        "*[value='Show more results']"
    )
    if show_more_button.is_displayed():
        show_more_button.click()
    if not len(browser.find_elements_by_css_selector(
        "*[data-status='3']")
    ) == 0:
        break
    browser.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)
    time.sleep(0.5)

# Extract image urls
images_src = []

for tag in browser.find_elements_by_css_selector(
    "div > div > div > a > div > img"
):
    src = tag.get_attribute('src')
    if src is None:
        src = tag.get_attribute('data-src')
    images_src.append(src)

browser.close()

urls, base64_strs, others = [], [], []

print(len(images_src))

for i, src in enumerate(images_src):
    if src.startswith('http'):
        urls.append(src)
    elif src.startswith('data'):
        base64_strs.append(src)
    else:
        others.append(src)

print(f'{len(urls)} urls, {len(base64_strs)} base64, {len(others)} others')

keyword = keyword.replace(' ', '_')

os.mkdir(keyword)
for i, url in enumerate(urls):
    res = requests.get(url)
    fileName = keyword + '_' + str(i+1).zfill(3)+'.jpeg'
    imageFile = open(os.path.join(keyword, fileName), 'wb')
    imageFile.write(res.content)
    imageFile.close()
    print(f'{i+1}/{len(urls)} images downloaded')
