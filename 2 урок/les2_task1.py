import requests
from bs4 import BeautifulSoup as BS
import re
from database.db import ArticleDB
from database.models import (
    Base,
    Article,
    Author,
    Tag,
)

start_url = 'https://geekbrains.ru'
url = 'https://geekbrains.ru/posts'


def url_on_page(url: str) -> tuple:
    def post_url_on_page(bs) -> list:
        lst = []
        temp = bs.find('div', attrs={'class': 'post-items-wrapper'})
        for item in temp.contents:
            # print(start_url + item.a['href'])
            lst.append(start_url + item.a['href'])
        return lst

    req = requests.get(url)
    soup = BS(req.text, 'lxml')
    tmp = soup.find('ul', attrs={'class': 'gb__pagination'}).find('li', attrs={'class': 'active'}).nextSibling
    # print(tmp)
    if tmp:
        # print(tmp.a['href'])
        next_page = start_url + tmp.a['href']
    else:
        next_page = ''
    return post_url_on_page(soup), next_page


def post_scraping(post_link: str):
    counter = 1
    req = requests.get(post_link)
    soup = BS(req.text, 'lxml')
    post_title = soup.h1.text.strip()
    print(post_title)
    post_date = soup.time.text.strip()
    print(post_date, post_link)

    tag_list = soup.article.find_all(attrs={'href': re.compile('^/posts\?tag=.+')})
    tags = []
    for item in tag_list:
        tag_name = item.text
        print(item.text, end=' ')
        tag_url = start_url + item['href']
        # print(item['href'])
        spam = db.session.query(Tag).filter_by(web_link=tag_url).first()
        if spam == None:
            tags.append(Tag(tag_name, tag_url))
        else:
            tags.append(spam)

    tmp = soup.article.find('div', attrs={'itemprop': 'author'})
    author_name = tmp.text
    print('\n' + author_name)
    author_link = start_url + tmp.parent['href']
    # print(author_link)
    spam = db.session.query(Author).filter_by(web_link=author_link).first()
    if spam == None:
        author = Author(author_name, author_link)
    else:
        author = spam

    spam = db.session.query(Article).filter_by(web_link=post_link).first()
    if spam == None:
        new_article = Article(post_title, post_date, post_link, author, tags)
    else:
        new_article = spam
    return new_article


common_post_url_list = []
counter = 1
while url:
    next_page_post_url_lst, next_page = url_on_page(url)
    for item in next_page_post_url_lst:
        if item not in common_post_url_list:
            common_post_url_list.append(item)
    url = next_page
    print('**********\tстраница № ' + str(counter) + '\t**********')
    counter += 1

db_path = 'sqlite:///article.sqlite'
db = ArticleDB(db_path)
counter = 0
post_count = len(common_post_url_list)
for post_url in common_post_url_list:
    new_post = post_scraping(post_url)
    db.session.add(new_post)
    db.session.commit()
    print('*************\tпост № ' + str(post_count - counter) + '\t*************')
    counter += 1
