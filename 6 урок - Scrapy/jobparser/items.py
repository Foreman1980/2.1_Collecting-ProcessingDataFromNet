# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    vacancy_name = scrapy.Field()
    vacancy_salary_above = scrapy.Field()
    vacancy_salary_below = scrapy.Field()
    vacancy_link = scrapy.Field()
    vacancy_source = scrapy.Field()

