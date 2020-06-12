import requests
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time

main_link = 'https://murmansk.hh.ru'

vacancy_info_dict = {'vacancy_title': None, 'vacancy_link': None, 'salary_min': None, 'salary_max': None,
                     'currency': None, 'employer': None, 'location': None,
                     }

def main():
    number_of_pages = 5
    vacancy = 'Data analyst'
    # vacancy = input('Введите наименование вакансии: ')

    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.\
    3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36',
               }

    params = {'L_is_autosearch': 'false', 'clusters': 'true', 'enable_snippets': 'true', 'salary': '',
              'st': 'searchVacancy', 'text': f'{vacancy}', 'fromSearch': 'true', 'page': '0',
              }

    link = main_link + '/search/vacancy'
    current_page_number = 0

    result_df = pd.DataFrame(data=vacancy_info_dict, index=[0])

    while (current_page_number < number_of_pages) and link != 'page not found':
        current_page_number += 1
        while True:
            page = requests.get(link, params=params, headers=headers)
            time.sleep(0.5)
            if page.status_code == 200:
                break
        page_html = page.text
        result_df = pd.concat([result_df, get_all_vacancy_from_page(page_html)], axis=0, ignore_index=True)
        print(get_all_vacancy_from_page(page_html))
        link = get_next_page_link(page_html)
        params = {}
    result_df = result_df.drop([0, 1], axis=0).reset_index(drop=True)
    result_df.to_excel('data.xls')


def get_all_vacancy_from_page(html: str) -> list:
    def vacancy_html_list(html: str) -> list:
        """Возвращает список из html-блоков с вакансиями"""
        all_vacancy_html = BS(html, 'lxml')
        return all_vacancy_html.find_all('div',
                                         attrs={'data-qa': ['vacancy-serp__vacancy vacancy-serp__vacancy_premium',
                                                            'vacancy-serp__vacancy']})

    def get_vacancy_title(bs_obj: BS) -> str:
        """Возвращает наименование вакансии"""
        return bs_obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text

    def get_vacancy_link(bs_obj: BS) -> str:
        """Возвращает ссылку на вакансию"""
        return bs_obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href'].split('?')[0]

    def get_vacancy_salary(bs_obj: BS) -> dict:
        """Возвращает словарь с минимальным и максимальным уровнем зарплаты, а также её валютой"""

        def parse_digit(string: str) -> int:
            value = ''
            for char in string:
                if char.isdigit():
                    value += char
            return int(value)

        try:
            salary = bs_obj.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        except AttributeError:
            salary = None

        salary_dict = {'salary_min': None, 'salary_max': None, 'currency': None}
        currency = ''
        if salary:
            for i in range(len(salary)):
                if not salary[::-1][i].isdigit():
                    currency += salary[::-1][i]
                else:
                    break
            salary_dict['currency'] = currency.strip()[::-1]
            if salary.find('-') == -1:
                salary_dict['salary_min'] = parse_digit(salary)
            else:
                min_value, max_value = salary.split('-')
                salary_dict['salary_min'] = parse_digit(min_value)
                salary_dict['salary_max'] = parse_digit(max_value)
        return salary_dict

    def get_vacancy_employer(bs_obj: BS) -> str:
        """Возвращает наименование работодателя"""
        return bs_obj.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.strip()

    def get_vacancy_location(bs_obj: BS) -> str:
        """Возвращает местоположение работодателя"""
        return bs_obj.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text

    df = pd.DataFrame(data=vacancy_info_dict, index=[0])
    for vacancy in vacancy_html_list(html):
        next_vacancy_info_dict = vacancy_info_dict
        next_vacancy_info_dict['vacancy_title'] = get_vacancy_title(vacancy)
        next_vacancy_info_dict['vacancy_link'] = get_vacancy_link(vacancy)
        salary_dict = get_vacancy_salary(vacancy)
        next_vacancy_info_dict['salary_min'] = salary_dict['salary_min']
        next_vacancy_info_dict['salary_max'] = salary_dict['salary_max']
        next_vacancy_info_dict['currency'] = salary_dict['currency']
        next_vacancy_info_dict['employer'] = get_vacancy_employer(vacancy)
        next_vacancy_info_dict['location'] = get_vacancy_location(vacancy)
        df = df.append(next_vacancy_info_dict, ignore_index=True)
    return df

def get_next_page_link(html: str) -> str:
    """Возвращает ссылку на следующую страницу результатов поиска"""
    bs_obj = BS(html, 'lxml')
    try:
        next_params = bs_obj.find('a', attrs={'data-qa': 'pager-next'})['href']
    except TypeError:
        return 'page not found'
    return main_link + next_params


if __name__ == '__main__':
    main()
