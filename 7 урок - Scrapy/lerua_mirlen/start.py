from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import sys

sys.path.insert(0,
                r"D:\Бизнес\15 Data-scientist (Phyton)\Занятия\GeekBrains\2.1_Collecting&ProcessingDataFromNet\7 урок - Scrapy")

from lerua_mirlen import settings
from lerua_mirlen.spiders.lmru import LmruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmruSpider, request='')  # request - доп. параметр, кот. можно принять при запуске start.py из консоли

    process.start()
