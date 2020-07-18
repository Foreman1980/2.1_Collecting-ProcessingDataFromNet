# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeruaMirlenDataBasePipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['leroymerlin']

    def process_item(self, item, spider):
        category = item['category'].split('/')[-1]
        collection = self.mongo_base[category]
        for i in range(len(item['specifications'])):
            item['specifications'][i] = f'{i + 1} {item["specifications"][i]}'
        spec_dict = dict(zip(item['specifications'], item['value']))
        item['specifications'] = spec_dict
        del item['value']
        collection.insert_one(item)
        return item


class LeruaMirlenPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img in item['photos']:
            try:
                yield scrapy.Request(img, meta=item)
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None):
        item = request.meta
        category = item['category'].split('/')[-1]
        return f'{category}/{item["full_name"]}/{request.url.split("/")[-1]}'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
