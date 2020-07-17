import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").extract_first()
        vacancy_list = response.css(
            'div.f-test-vacancy-item a::attr(href)').extract()  # //div[contains(@class, 'f-test-vacancy-item')]//a/@href

        for link in vacancy_list:
            if link.startswith('/vakansii/'):
                yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_job = response.xpath('//h1/text()').extract_first()
        salary_job = response.xpath(
            "//div[contains(@class, 'f-test-vacancy-base-info')]/div[2]/div[contains(@class, 'undefined')]/div/div/child::node()[5]/span[1]/span/text()").extract()
        link_job = response.url
        source_job = 'superjob.ru'
        yield JobparserItem(vacancy_name=name_job, vacancy_salary_above=salary_job, vacancy_salary_below='',
                            vacancy_link=link_job, vacancy_source=source_job)
