from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from datetime import date, timedelta
from pymongo import MongoClient
from pprint import pprint
import time


def main():
    options = webdriver.ChromeOptions()
    binary_yandex_driver_file = 'yandexdriver.exe'

    with webdriver.Chrome(binary_yandex_driver_file, options=options) as driver:
        wait = WebDriverWait(driver, 5)
        driver.maximize_window()
        driver.get('https://mail.ru/')

        # Авторизация в почте
        driver.find_element_by_id('mailbox:login').send_keys('study.ai_172@mail.ru' + Keys.RETURN)
        wait.until(EC.element_to_be_clickable((By.ID, 'mailbox:password'))).send_keys('NextPassword172' + Keys.RETURN)

        # Открываем первое письмо в списке писем
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'llc__container'))).click()

        # time.sleep(0.5) # вроде работает и без этой паузы

        # запоминаем id первого письма
        letter_id = next_letter_id = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'thread__letter_expanded'))).get_attribute('data-id')

        count = 0
        next_letter_is_open = True
        while next_letter_is_open:
            # Парсим всю нужную информацию из текущего письма (запись в БД полученного словаря реализована в функции)
            letter_dict = get_letters_data(driver, letter_id)

            # Счётчик писем (на 24.06.2020 их 334 шт.) Почему-то парсит только 333...одно письмо проскакивает что ли?...
            # Действительно проскакивал...со второго прохода в базе 334 письма...как?...видимо не сработала строка 62...
            # Если одно письмо пропускает, может и пять пропустить...может другое EC-условие использовать...
            count += 1

            # Тестовый вывод
            print('№', count, '*' * 50)
            del letter_dict['letters_body']  # удаляю, для сокращения тестового вывода
            pprint(letter_dict)
            print('*' * (len(f'№ {count} ') + 50))

            # Не разобрался как однозначно определить, что письмо прогрузилось, пришлось мудрить
            while letter_id == next_letter_id:
                # сплагиатил способ перемещения по письмам из разбора д/з
                element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button2_arrow-down')))
                try:
                    element.click()
                except ElementClickInterceptedException:
                    next_letter_is_open = False
                    break
                else:
                    time.sleep(0.5)  # без этой паузы работать не хочет...
                    next_letter_id = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'thread__letter_expanded'))).get_attribute(
                        'data-id')
            else:
                letter_id = next_letter_id


def get_letters_data(drv: webdriver, letter_id: str) -> dict:
    """Получение необходимых данных из письма, формирование словаря и сохранение в БД"""

    letter_dict = {}

    letter_dict['_id'] = letter_id

    letter_dict['letters_sender'] = WebDriverWait(drv, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='letter__author']/span[@class='letter-contact']"))).get_attribute('title')

    letter_dict['receiving_date'] = date_convert(WebDriverWait(drv, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@class='letter__author']/div[@class='letter__date']"))).text)

    letter_dict['letters_topic'] = WebDriverWait(drv, 5).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'thread__subject')]"))).text

    # id-письма пригодился
    letter_dict['letters_body'] = WebDriverWait(drv, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//div[@id='style_{letter_id}_BODY']"))).text

    # делаем запись в БД
    letters.update_one({'_id': letter_dict['_id']}, {'$set': letter_dict}, upsert=True)
    return letter_dict


def date_convert(string: str) -> str:
    """Обработка даты, приведение к единому стандарту"""

    month = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня', 7: 'июля',
             8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'}
    if string.startswith('Сегодня'):
        return string.replace('Сегодня', f'{date.today().day} {month[date.today().month]} {date.today().year}')
    elif string.startswith('Вчера'):
        return string.replace(
            'Вчера',
            f'{(date.today() - timedelta(days=1)).day} {month[(date.today() - timedelta(days=1)).month]} {(date.today() - timedelta(days=1)).year}')
    else:
        date_list = string.split(',')[0].split(' ')
        if len(date_list) == 2:
            date_list.append(str(date.today().year))
            return ','.join((' '.join(date_list), string.split(',')[1]))
        else:
            return string


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client['mail_db']
    letters = db.mail

    main()
