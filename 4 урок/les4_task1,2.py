import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime, date
import time

news_link_mail = 'https://news.mail.ru'
news_link_lenta = 'https://lenta.ru'
news_link_yandex = 'https://yandex.ru/news'

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
 Chrome/81.0.4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Safari/537.36',
           }

client = MongoClient('localhost', 27017)
db = client['news_db']
news = db.news


def pars_news_mail():
    def get_all_news_links_on_start_page(page_html: str) -> list:
        dom = html.fromstring(page_html)
        blocks = dom.xpath("//a[@class='photo photo_full photo_scale js-topnews__item'] | \
        //a[@class='photo photo_small photo_scale photo_full js-topnews__item'] | \
        //ul[@class='list list_type_square list_half js-module']/li[not(contains(@class, 'hidden_medium hidden_large'))] | \
        //a[@class='newsitem__title link-holder'] | //a[@class='link link_flex']")
        links_on_start_page = []
        for block in blocks:
            link = block.xpath('.//@href')
            if len(link[0].split('/')) == 4:
                links_on_start_page += link
        return links_on_start_page

    def get_news_data(news_link: str) -> dict:
        news_dict = {}
        response = requests.get(news_link, headers=headers)
        news_dom = html.fromstring(response.text)
        news_dict['news_headline'] = news_dom.xpath("//h1[@class='hdr__inner']/text()")[0]
        news_dict['source_name'] = news_dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span/text()")[0]
        news_dict['news_date'] = convert_news_date(
            news_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0])
        news_dict['news_link'] = news_link
        news_dict['updated_date'] = date.today().strftime('%d.%m.%Y')
        return news_dict

    response = requests.get(news_link_mail, headers=headers)
    news_links = get_all_news_links_on_start_page(response.text)
    for link in news_links:
        news_data_dict = get_news_data(news_link_mail + link)
        time.sleep(1)
        news.update_one({'news_link': news_data_dict['news_link']}, {'$set': news_data_dict}, upsert=True)
        pprint(news_data_dict)


def pars_news_lenta():
    def get_all_news_links_on_start_page(page_html: str) -> list:
        dom = html.fromstring(page_html)
        blocks = dom.xpath("//div[contains(@class, 'item')]//a[contains(@href, 'news')]")
        links_on_start_page = []
        for block in blocks:
            link = block.xpath('.//@href')
            if link[0].startswith('/news/'):
                links_on_start_page += link
        return links_on_start_page

    def get_news_data(news_link: str) -> dict:
        news_dict = {}
        response_news_page = requests.get(news_link, headers=headers)
        news_dom = html.fromstring(response_news_page.text)
        news_dict['news_headline'] = news_dom.xpath("//h1[contains(@class, 'b-topic__title')]/text()")[0].replace(
            '\xa0', ' ')
        news_dict['source_name'] = 'Lenta.RU'
        news_dict['news_date'] = convert_news_date(
            news_dom.xpath("//div[contains(@class, 'b-topic__info')]//@datetime")[0])
        news_dict['news_link'] = news_link
        news_dict['updated_date'] = date.today().strftime('%d.%m.%Y')
        return news_dict

    response = requests.get(news_link_lenta, headers=headers)
    news_links = get_all_news_links_on_start_page(response.text)
    for link in news_links:
        news_data_dict = get_news_data(news_link_lenta + link)
        time.sleep(1)
        news.update_one({'news_link': news_data_dict['news_link']}, {'$set': news_data_dict}, upsert=True)
        pprint(news_data_dict)


def pars_news_yandex():
    pass


def convert_news_date(date: str) -> str:
    return datetime.strptime(date.split('+')[0], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y')


def delete_old_news():
    """Перед окончанием работы программы, проверка и удаление закрытых на сайте вакансий"""

    result = news.delete_many({'updated_date': {'$ne': date.today().strftime('%d.%m.%Y')}})
    print(f'Удалено {result.deleted_count} устаревших записей.')


if __name__ == '__main__':
    pars_news_mail()
    pars_news_lenta()
    pars_news_yandex()
    delete_old_news()