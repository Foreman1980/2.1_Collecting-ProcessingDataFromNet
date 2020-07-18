import scrapy
from scrapy.http import HtmlResponse

from lerua_mirlen.items import LeruaMirlenItem
from scrapy.loader import ItemLoader
import time


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['https://leroymerlin.ru/catalogue/dreli-shurupoverty/']
    # start_urls = ['https://leroymerlin.ru/catalogue/ushm-bolgarki/']
    # start_urls = ['https://leroymerlin.ru/catalogue/teploizolyaciya/']
    start_urls = ['https://leroymerlin.ru/catalogue/vagonka/']

    # def __init__(self):
    #     self.start_urls = [f'https://leroymerlin.ru/catalogue/{request[0]}/']

    def parse(self, response: HtmlResponse):
        time.sleep(1)
        next_page = response.css('a.next-paginator-button::attr(href)').extract_first()
        product_links = response.css(
            'div.plp-card-list-inner div.ui-sorting-cards div.ui-product-card__info a::attr(href)').extract()

        for link in product_links:
            yield response.follow(link, callback=self.product_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaMirlenItem(), response=response)
        loader.add_xpath('category', '//uc-breadcrumbs-link/a/@data-division')
        loader.add_xpath('full_name', '//h1/text()')
        loader.add_xpath('specifications', '//uc-pdp-section-layout//dt[@class="def-list__term"]/text()')
        loader.add_xpath('value', '//uc-pdp-section-layout//dd[@class="def-list__definition"]/text()')
        loader.add_xpath('price', '//uc-pdp-price-view//meta[@itemprop="price"]/@content')
        loader.add_xpath('photos', '//picture//source[1]/@data-origin')
        loader.add_value('link', response.url)
        yield loader.load_item()
