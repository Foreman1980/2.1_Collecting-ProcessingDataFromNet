# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies_scrapy']

    def process_item(self, item, spider):
        vacancy_salary = item['vacancy_salary_above']
        if spider.name == 'hhru':
            if len(vacancy_salary) == 7:
                item['vacancy_salary_above'] = vacancy_salary[1].replace('\xa0', '') + vacancy_salary[4] + \
                                               vacancy_salary[5]
                item['vacancy_salary_below'] = vacancy_salary[3].replace('\xa0', '') + vacancy_salary[4] + \
                                               vacancy_salary[5]
            elif len(vacancy_salary) == 5:
                item['vacancy_salary_above'] = vacancy_salary[1].replace('\xa0', '') + vacancy_salary[2] + \
                                               vacancy_salary[3]
                item['vacancy_salary_below'] = 'з/п не указана'
            else:
                item['vacancy_salary_above'] = 'з/п не указана'
                item['vacancy_salary_below'] = 'з/п не указана'
        else:
            if len(vacancy_salary) == 4:
                item['vacancy_salary_above'] = vacancy_salary[0].replace('\xa0', '') + ' ' + vacancy_salary[3]
                item['vacancy_salary_below'] = vacancy_salary[1].replace('\xa0', '') + ' ' + vacancy_salary[3]
            elif len(vacancy_salary) == 3:
                salary = vacancy_salary[2].split('\xa0')
                if vacancy_salary[0] == 'от':
                    item['vacancy_salary_above'] = salary[0] + salary[1] + ' ' + salary[2]
                    item['vacancy_salary_below'] = 'з/п не указана'
                else:
                    item['vacancy_salary_above'] = 'з/п не указана'
                    item['vacancy_salary_below'] = salary[0] + salary[1] + ' ' + salary[2]
            else:
                item['vacancy_salary_above'] = 'з/п не указана'
                item['vacancy_salary_below'] = 'з/п не указана'
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
