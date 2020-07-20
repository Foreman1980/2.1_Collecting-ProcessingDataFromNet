# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['instagram']

    def process_item(self, item, spider):
        collection = self.mongo_base['users']

        # На случай взаимной подписки (c исследуемым пользователем), чтобы не задублировать пользователя, а только
        # обновить списки подписок (для примера см. 'noxlis')
        result = collection.find_one({'user_id': item['user_id']})
        if result:
            if result['followers']:
                followers_list = item['followers']
                followers_list.extend(result['followers'])
                item['followers'] = list(set(followers_list))
            elif result['following']:
                following_list = item['following']
                following_list.extend(result['following'])
                item['following'] = list(set(following_list))
        collection.update_one({'user_id': item['user_id']}, {'$set': item}, upsert=True)
        return item
