import requests
from bs4 import BeautifulSoup
import json
import csv
import os

url = 'https://smolensk.jsprav.ru'

req = requests.get(url)
src = req.text

soup = BeautifulSoup(src, 'lxml')
sections = soup.find_all(class_='col-sm-6')

all_categories_dict = {}

for item in sections:
    item_text = item.find('a').find('span').text.strip()
    item_link = item.find('a').get('href')

    all_categories_dict[item_text] = url + item_link
    print(item_text, item_link)

    with open('data2.json', 'w', encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

res_dict = {}
with open('data2.json', encoding='utf-8') as file:
    all_categories = json.load(file)

for category_title, category_link in all_categories.items():

    rep = [' ', ',', "'", '-']

    for item in rep:
        if item in category_title:
            category_title = category_title.replace(item, '_')

    req = requests.get(category_link)
    src = req.text

    soup = BeautifulSoup(src, 'lxml')

    category_level = soup.find(class_='category-level0').find('h1').text

    json_dict = {}
    links_links = []

    cat_item = soup.find_all(class_='cat-item')
    for item in cat_item:
        item_inner = item.find('a').find('span').nextSibling.strip()
        item_link = item.find('a').get('href')

        item_dict = {}
        item_dict[item_inner] = url + item_link
        links_links.append(item_dict)

    json_dict[category_level] = links_links
    res_dict[category_title] = json_dict

with open('category_data.json', 'a', encoding='utf-8') as file:
    json.dump(res_dict, file, indent=4, ensure_ascii=False)

with open('category_data.json', encoding='UTF-8') as file:
    all_categories = json.load(file)

count = 0
for key in all_categories.values():
    for key2 in key.values():
        for category in key2:
            for category_title, category_link in category.items():

                rep = [' ', ',', "'", '-', '/', '\\']

                for item in rep:
                    if item in category_title:
                        category_title = category_title.replace(item, '_')

                req = requests.get(category_link)
                src = req.text

                with open(f'data2/{count}_{category_title}.html', 'w', encoding='UTF-8') as file:
                    file.write(src)

                with open(f'data2/{count}_{category_title}.html', encoding='UTF-8') as file:
                    src = file.read()

                soup = BeautifulSoup(src, 'lxml')

                orgs_data_dict = {}
                with open(f'data2/{count}_{category_title}.csv', 'w', encoding='UTF-8') as file:
                    writer = csv.writer(file)
                    writer.writerow((
                        'Название:',
                        'Адрес:',
                        'Номер телефона:',
                        'график (часы) работы:',
                        'официальный сайт:',
                        'электронная почта:'
                    ))

                orgs = soup.find_all(class_='org')
                for item in orgs:
                    title = item.find(class_='lnk').text.strip()
                    # adress_list = []
                    adress = item.find(class_='last').find_all('p')
                    # for a in adress:
                    #     adress_list.append(a.text)
                    adres = ''
                    phone_number = ''
                    schedule = ''
                    off_site = ''
                    mail = ''
                    if len(adress) > 0:
                        adres = adress[0].text.strip()
                        if len(adress) > 1:
                            phone_number = adress[1].text.strip()
                        if len(adress) > 2:
                            schedule = adress[2].text.strip()
                        if len(adress) > 3:
                            off_site = adress[3].text.strip()
                        if len(adress) > 4:
                            mail = adress[4].text.strip()

                    with open(f'data2/{count}_{category_title}.csv', 'a', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow((
                            title,
                            adres,
                            phone_number,
                            schedule,
                            off_site,
                            mail
                        ))

                    print(title, adres, phone_number, schedule, off_site, mail)

    count += 1
