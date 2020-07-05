import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from datetime import date
from pprint import pprint

# Константа, задающая домашнйи регион
HOME_CITY = 'Мурманск'


def main():
    options = webdriver.ChromeOptions()
    binary_yandex_driver_file = 'yandexdriver.exe'

    with webdriver.Chrome(binary_yandex_driver_file, options=options) as driver:
        wait = WebDriverWait(driver, 5)
        driver.maximize_window()
        driver.get('https://www.mvideo.ru/')

        # Выбираем домашний регион
        driver.find_element_by_class_name('btn-choice-other-city').click()
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'city-input'))).send_keys(HOME_CITY + Keys.ENTER)
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-city-submit-btn'))).click()

        # Сохраняем количество возможных прокруток карусели
        carousel_link_list = driver.find_elements_by_xpath(
            "//div[@class='gallery-layout'][2]//div[@class='carousel-paging']/a")

        # Переводим карусель прокрутки в крайнее положение, при кот. на странице прогружены все ссылки на товары из
        # интересующей группы "Хиты продаж"
        wait.until(EC.element_to_be_clickable((By.XPATH,
                                               f"//div[@class='gallery-layout'][2]//div[@class='carousel-paging']/a[{len(carousel_link_list)}]"))).click()

        time.sleep(2)
        # Забираем все прогрузившиеся ссылки на товары из категории "Хиты продаж"
        current_product_link_list = driver.find_elements_by_xpath(
            "//div[@class='gallery-layout'][2]//li//div[@class='c-product-tile-picture__holder']/a")

        for link in current_product_link_list:
            product_data = json.loads(link.get_attribute('data-product-info'))
            product_data['productLink'] = link.get_attribute('href')
            product_data['entryDate'] = date.today().strftime('%d.%m.%Y')
            pprint(product_data)
            print()

            # делаем запись в БД
            products.update_one({'productId': product_data['productId']}, {'$set': product_data}, upsert=True)


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['bestsellers_db']
    products = db.products

    main()
