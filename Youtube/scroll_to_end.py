from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

binary = r"C:\Program Files\Mozilla Firefox\firefox.exe"
options = webdriver.FirefoxOptions()
options.binary = binary

driver = webdriver.Firefox(options=options)

# navigate to the URL
driver.get("https://www.youtube.com/@BrianScott1111/videos")

# wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body")))

# simulate a user scrolling down the page
scroll_delay = 1
scroll_distance = 100

while True:
    driver.execute_script("window.scrollBy(0, {})".format(scroll_distance))
    time.sleep(scroll_delay)

    # check if the bottom of the page has been reached
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == driver.execute_script("return window.pageYOffset + window.innerHeight"):
        break

# close the browser
driver.quit()
