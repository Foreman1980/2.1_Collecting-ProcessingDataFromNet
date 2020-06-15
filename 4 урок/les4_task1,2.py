import requests
from lxml import html
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
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
        # //ul[@class='list list_type_square list_half js-module']/li
        dom = html.fromstring(page_html)
        blocks = dom.xpath("//a[@class='photo photo_full photo_scale js-topnews__item'] | \
        //a[@class='photo photo_small photo_scale photo_full js-topnews__item'] | \
        //ul[@class='list list_type_square list_half js-module']/li[not(contains(@class, 'hidden_medium hidden_large'))] | \
        //a[@class='newsitem__title link-holder'] | \
        //a[@class='link link_flex']")
        links_on_start_page = []
        for block in blocks:
            link = block.xpath('.//@href')
            links_on_start_page += link
        return links_on_start_page

    def get_news_data(news_link: str) -> dict:
        news_dict = {}
        response = requests.get(news_link, headers=headers)
        news_dom = html.fromstring(response.text)
        news_dict['news_headline'] = news_dom.xpath("//h1[@class='hdr__inner']/text()")[0]
        news_dict['source_name'] = news_dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span/text()")[0]
        news_date = news_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
        news_dict['news_date'] = datetime.strptime(news_date.split('+')[0], '%Y-%m-%dT%H:%M:%S').strftime('%d.%m.%Y')
        news_dict['news_link'] = news_link
        return news_dict

    response = requests.get(news_link_mail, headers=headers)
    news_links = get_all_news_links_on_start_page(response.text)
    for link in news_links:
        news_data_dict = get_news_data(news_link_mail + link)
        time.sleep(1)
        news.update_one({'news_link': news_data_dict['news_link']}, {'$set': news_data_dict}, upsert=True)
        pprint(news_data_dict)


def pars_news_lenta():
    pass


def pars_news_yandex():
    pass


if __name__ == '__main__':
    pars_news_mail()
    pars_news_lenta()
    pars_news_yandex()
