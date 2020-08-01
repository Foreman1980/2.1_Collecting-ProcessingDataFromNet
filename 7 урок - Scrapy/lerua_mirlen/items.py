# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def price_processing(product_price: str) -> float:
    price = product_price.replace(' ', '').split('.')
    return int(price[0]) + int(price[1])/100


def name_processing(product_name: str) -> str:
    return product_name.replace('\n', '')


def value_processing(specifications_value: str) -> str:
    return specifications_value.replace('\n', '').strip()


class LeruaMirlenItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    category = scrapy.Field(input_processor=Join('/'), output_processor=TakeFirst())
    full_name = scrapy.Field(input_processor=MapCompose(name_processing), output_processor=TakeFirst())
    specifications = scrapy.Field()
    value = scrapy.Field(input_processor=MapCompose(value_processing))
    price = scrapy.Field(input_processor=MapCompose(price_processing), output_processor=TakeFirst())
    photos = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
