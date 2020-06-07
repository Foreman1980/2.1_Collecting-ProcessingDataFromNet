import requests
import json

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.\
4044.138 YaBrowser/20.6.0.905 Yowser/2.5 Safari/537.36'}
user_name = 'Foreman1980'
url = f'https://api.github.com/users/{user_name}/repos'

response = requests.get(url, headers=headers)

my_repo_list = []
for item in response.json():
    my_repo_list.append(item['full_name'])

with open('my_repo.json', 'w', encoding='utf-8') as f:
    json.dump(my_repo_list, f)
