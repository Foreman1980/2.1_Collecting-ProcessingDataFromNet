import requests
import json

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.2.252 Yowser/2.5 Safari/537.36'}
url = 'https://api.github.com/users/Foreman1980/repos'

response = requests.get(url, headers=headers)

my_repo_list = []
for item in response.json():
    my_repo_list.append(item['full_name'])

with open('my_repo.json', 'w', encoding='utf-8') as f:
    json.dump(my_repo_list, f)
