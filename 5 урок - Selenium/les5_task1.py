from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time

options = webdriver.ChromeOptions()
binary_yandex_driver_file = 'yandexdriver.exe'
driver = webdriver.Chrome(binary_yandex_driver_file, options=options)
driver.maximize_window()
driver.get('https://mail.ru/')

login_form = driver.find_element_by_id('mailbox:login')
login_form.send_keys('study.ai_172@mail.ru')
login_form.send_keys(Keys.RETURN)
password_form = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'mailbox:password')))
password_form.send_keys('NextPassword172')
password_form.send_keys(Keys.RETURN)

first_letter = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'llc__container')))
first_letter.click()
time.sleep(0.5)
letter_id = driver.find_element_by_class_name('thread__letter_expanded').get_attribute('data-id')
count = 1

while True:
    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'button2_arrow-down')))
    try:
        element.click()
    except ElementClickInterceptedException:
        break
    else:
        print(count, letter_id)
        time.sleep(0.5)
        count += 1
        letter_id = driver.find_element_by_class_name('thread__letter_expanded').get_attribute('data-id')

# driver.find_element_by_class_name('button2_has-ico button2_arrow-down').click()
# driver.quit()
