#! python3

# imageScrapper.py - fetching numbers of images from
# duckduckgo based on given keyword.

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, os
import pyinputplus as pyip

baseUrl = 'https://duckduckgo.com/?t=h_&iax=images&ia=images&q='

# Get user input for keyword and number of images
keyword = pyip.inputStr('Enter a keyword :')
number_of_images = pyip.inputInt('How much images do you want to download?')

# Opening the web
browser = webdriver.Chrome()
browser.get(baseUrl + keyword)

# Scroll to the end of the page to get more images
for _i in range(6):
    browser.find_element_by_xpath('//body').send_keys(Keys.CONTROL+Keys.END)
    time.sleep(2)

# Putting all the image links into a list
imageUrls = []
for tag in browser.find_elements_by_css_selector('.tile--img__img'):
    imageUrls.append(tag.get_attribute('src'))
browser.quit()

# Compare number of result to user request. pick the smaller.
number_of_images = min(len(imageUrls), number_of_images)

# Reduce the list size to match number_of_images
imageUrls = imageUrls[:number_of_images]

# Download the image
os.mkdir(keyword)
print('Downloading %s images' %number_of_images)
for i, url in enumerate(imageUrls):
    res = requests.get(url)
    try:
        res.raise_for_status()
    except:
        print('an error occured, please try again')
        exit()
    # Save the image
    imageFile = open(os.path.join(keyword, keyword+'_'+str(i+1).zfill(len(str(number_of_images)))+'.jpeg'), 'wb')
    for chunk in res.iter_content(100000):
        imageFile.write(chunk)
    imageFile.close()
    print(f'Downloaded {i+1}/{number_of_images}')
print('\nDownload Complete')