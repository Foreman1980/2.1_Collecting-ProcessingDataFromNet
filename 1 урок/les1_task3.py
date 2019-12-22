import requests
import time
import json


def get_data(url, headers):
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        time.sleep(0.5)
    return response.json()


def get_product_list(categiry):
    results = []
    new_url = url + f'?page=1&categories={categiry}'
    while new_url:
        response = get_data(new_url, headers)
        results.extend(response['results'])
        new_url = response['next']
    return results


headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36'}

url = 'https://5ka.ru/api/v2/special_offers/'
url_category = 'https://5ka.ru/api/v2/categories/'

product_category = {'category_id': '', 'category_name': ''}
product_category_list = []

response_cat = requests.get(url_category, headers=headers)

print(response_cat.json())

for item in response_cat.json():
    product_category['category_id'] = item['parent_group_code']
    cat_name = item['parent_group_name']
    if len(cat_name.split('\n')) > 1:
        char = cat_name.find('*\n* Кроме')
        cat_name = cat_name[1:char] + ' (Кроме детских)'
    product_category['category_name'] = cat_name
    product_category_list.append(product_category.copy())

for dct in product_category_list:
    with open(f'{dct["category_id"]}_{dct["category_name"]}.json', 'w', encoding='utf-8') as f:
        json.dump(get_product_list(dct['category_id']), f, ensure_ascii=False)
