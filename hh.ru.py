#Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайта HH.
# Приложение должно анализировать все страницы сайта. Получившийся
# список должен содержать в себе минимум:
#Наименование вакансии.
#Предлагаемую зарплату (разносим в три поля: минимальная и
# максимальная и валюта. цифры преобразуем к цифрам).
#Ссылку на саму вакансию.
#Сайт, откуда собрана вакансия.
#По желанию можно добавить ещё параметры вакансии
# (например, работодателя и расположение). Общий результат можно вывести
# с помощью dataFrame через pandas. Сохраните в json либо csv.

from bs4 import BeautifulSoup as bs
import re
import requests
from pprint import pprint
import pandas as pd
base_url='https://hh.ru'
main_url='https://hh.ru/search/vacancy'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
params={'page':0}
while True:
    session=requests.Session()
    response=session.get(main_url, headers=headers,params=params)
    print(response)

    dom=bs(response.text,'html.parser')
    vacancies = dom.find_all('div', {'class': 'serp-item'})
    print(len(vacancies))
    if len(vacancies)==0:
        break
    #params['page'] +=1
    vacancy_list=[]
    for vacancy in vacancies:
        vacancy_data={}
        title=vacancy.find('a',{'class': 'serp-item__title'})
        link=title['href']
        name_vacancy=title.getText()
        site= 'hh.ru'
        #salary=vacancy.find('span',{'class':'bloko-header-section-3'})#.getText()
        salary=vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})#.getText()
        town=vacancy.find('div', {'data-qa':'vacancy-serp__vacancy-address'}).getText()
        employer=vacancy.find('div', {'class':'vacancy-serp-item__meta-info-company'}).getText().replace('\xa0',' ')
        if not salary:
            salary_min = None
            salary_max = None
            salary_currency = None
        else:
            salary = salary.getText() \
                .replace(u'\xa0', u'')

            salary = re.split(r'\s|-', salary)
            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_max = None
            else:
                salary_min = int(salary[0])
                salary_max = (salary[1])
            salary_currency = salary[2]

        vacancy_data['salary_min'] = salary_min
        vacancy_data['salary_max'] = salary_max
        vacancy_data['salary_currency'] = salary_currency
    #print(salary)

        vacancy_data['name_vacancy']=name_vacancy
        vacancy_data['link'] = link
        vacancy_data['salary'] = salary
        vacancy_data['site'] = site
        vacancy_data['town'] = town
        vacancy_data['employer'] = employer
        vacancy_list.append(vacancy_data)
    params['page'] +=1
pprint(vacancy_list)
print(pd.DataFrame.from_dict(vacancy_list
                             ))
