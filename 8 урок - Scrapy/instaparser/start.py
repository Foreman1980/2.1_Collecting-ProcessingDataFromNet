from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import sys

sys.path.insert(0,
                r"D:\Бизнес\15 Data-scientist (Phyton)\Занятия\GeekBrains\2.1_Collecting&ProcessingDataFromNet\8 урок - Scrapy")

from instaparser import settings
from instaparser.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider)

    process.start()
