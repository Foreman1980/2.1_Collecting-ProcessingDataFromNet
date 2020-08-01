from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['instagram']
users = db.users


def following_search(user_name: str):
    """Возвращает всех подписчиков пользователя"""
    for user in users.find({'following': {'$eq': 'kumzhev'}}):
        pprint(user)

def followers_search(user_name: str):
    """Возвращает всех подписанных на пользователя"""
    for user in users.find({'followers': {'$eq': 'kumzhev'}}):
        pprint(user)

def mutually_followers_search(user_name: str):
    """Возвращает всех взаимно подписанных друг на друга пользователей"""
    for user in users.find({'$and': [{'followers': {'$eq': 'kumzhev'}}, {'following': {'$eq': 'kumzhev'}}]}):
        pprint(user)

if __name__ == '__main__':
    # following_search('kumzhev')
    # followers_search('kumzhev')
    mutually_followers_search('kumzhev')
