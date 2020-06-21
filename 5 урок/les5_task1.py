from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
binary_yandex_driver_file = 'yandexdriver.exe'
driver = webdriver.Chrome(binary_yandex_driver_file, options=options)
driver.get('https://mail.ru/')

element = driver.find_element_by_id('mailbox:login')
element.send_keys('study.ai_172@mail.ru')
element.send_keys(Keys.RETURN)
time.sleep(1)
element = driver.find_element_by_id('mailbox:password')
element.send_keys('NextPassword172')
element.send_keys(Keys.RETURN)







# driver.quit()
