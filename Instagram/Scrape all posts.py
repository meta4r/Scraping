import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)

driver.get("https://www.instagram.com/accounts/login/")

wait = WebDriverWait(driver, 10)
username = wait.until(EC.presence_of_element_located((By.NAME, "username")))
password = wait.until(EC.presence_of_element_located((By.NAME, "password")))

# credentials
username.send_keys("")
password.send_keys("")

password.send_keys(Keys.RETURN)

button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]")))
button.click()

url = 'https://www.instagram.com/" "/' #target
profile_name = url.split('/')[-2]

driver.get("https://www.instagram.com/{}/".format(profile_name))

# Wait for the page to load
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

if not os.path.exists(profile_name):
    os.makedirs(profile_name)

img_tags = soup.find_all('img')

post_count_element = soup.select_one("span[title='Posts'] > span")
if post_count_element:
    post_count = int(post_count_element.text.replace(',', ''))
else:
    post_count = 0

# Scroll down the page to load more posts
for i in range(post_count//12 + 1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

SCROLL_PAUSE_TIME = 3

#  Scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse page source to BeautifulSoup object
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Get image tags
img_tags = soup.find_all('img')

# Get image URLs
urls = [img['src'] for img in img_tags if '.jpg' in img['src']]

# Download images
for i, url in enumerate(urls):
    response = requests.get(url)
    with open(f'{profile_name}/img_{i}.jpg', 'wb') as f:
        f.write(response.content)

driver.quit()