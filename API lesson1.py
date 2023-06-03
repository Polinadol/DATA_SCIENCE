#_ 1. Посмотреть документацию к API GitHub, разобраться
# как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
# https://api.github.com/users/USERNAME/repos



import requests

import json

def get_data(url: str) -> dict:
    while True:
        time.sleep(1)
        response = requests.get(url)
        if response.status_code == 200:
            break
    return response.json()

user = input('Введите пользователя: ')
user = 'Polinadol' if user == '' else user
url = 'https://api.github.com/users/'+user+'/repos'

response = get_data(url)


repo = []
for i in response:
    repo.append(i['name'])
print(f'Список репозиториев  {user}')
print(repo)

with open('user.json', 'w') as f:
    json_repo = json.dump(repo, f)