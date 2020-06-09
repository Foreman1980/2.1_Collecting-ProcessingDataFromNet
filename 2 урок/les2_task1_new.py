import requests
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time


def main():
    number_of_pages = 1
    vacancy = 'Data analyst'
    # vacancy = input('Введите наименование вакансии: ')

    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.\
    3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36'}

    params = {'L_is_autosearch': 'false', 'clusters': 'true', 'enable_snippets': 'true', 'salary': '',
              'st': 'searchVacancy', 'text': f'{vacancy}', 'fromSearch': 'true', 'page': '0',
              }

    main_link = 'https://murmansk.hh.ru/search/vacancy'

    link = main_link
    current_page_number = 0

    vacancy_info_dict = {'vacancy_name': [None], 'vacancy_link': [None], 'salary_min': [None], 'salary_max': [None],
                         'currency': [None], 'employer': [None], 'location': [None]}

    result_df = pd.DataFrame(data=vacancy_info_dict)

    while current_page_number < number_of_pages:
        current_page_number += 1
        page_html = requests.get(main_link, params=params, headers=headers).text
        # result_df = pd.concat([result_df, get_all_vacancy_from_page(page_html)], axis=0, ignore_index=True)
        print(get_all_vacancy_from_page(page_html))
        time.sleep(0.5)


def get_all_vacancy_from_page(html: str) -> list:
    def vacancy_html_list(html: str) -> list:
        """Возвращает список из html-блоков с вакансиями"""
        all_vacancy_html = BS(html, 'lxml')
        return all_vacancy_html.find_all('div',
                                         attrs={'data-qa': ['vacancy-serp__vacancy vacancy-serp__vacancy_premium',
                                                            'vacancy-serp__vacancy']})

    def get_vacancy_title(bs_obj: BS) -> str:
        """Возвращает список из html-блоков с вакансиями"""
        return bs_obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text

    def get_vacancy_link(bs_obj: BS) -> str:
        """Возвращает список из html-блоков с вакансиями"""
        return bs_obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href'].split('?')[0]

    def get_vacancy_salary(bs_obj: BS) -> str:
        """Возвращает список из html-блоков с вакансиями"""
        salary = None
        try:
            salary = bs_obj.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        except AttributeError:
            pass
        return salary

    def get_vacancy_employer(bs_obj: BS) -> str:
        """Возвращает наименование работодателя"""
        return bs_obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text

    def get_vacancy_location(bs_obj: BS) -> str:
        """Возвращает местоположение работодателя"""
        pass

    vacancy_title_list = []
    for vacancy in vacancy_html_list(html):
        print(get_vacancy_title(vacancy), get_vacancy_link(vacancy), get_vacancy_salary(vacancy),
              get_vacancy_employer(vacancy))
    return vacancy_html_list(html)


def get_next_page_link(html: str) -> str:
    """Возвращает ссылку на следующую страницу результатов поиска"""
    pass


if __name__ == '__main__':
    main()
