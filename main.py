import requests
from bs4 import BeautifulSoup
import json
import csv

url = 'https://smolensk.jsprav.ru'
# req = requests.get(url)
# src = req.text
#
# soup = BeautifulSoup(src, 'lxml')
# section = soup.find(class_='cats-list')
#
# links = section.find_all('li')
#
# all_categories_dict = {}
#
# for item in links:
#     item_text = item.find('a').find('span')
#     item_link = item.find('a').get('href')
#
#     if item_text != None:
#         item_text = item_text.nextSibling.strip()
#         all_categories_dict[item_text] = url + item_link
#
# with open('datat.json', 'w', encoding='UTF-8') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open('datat.json', encoding='UTF-8') as file:
    all_categories = json.load(file)

count = 0

for category_title, category_link in all_categories.items():

    rep = [' ', ',', "'", '-']

    for item in rep:
        if item in category_title:
            category_title = category_title.replace(item, '_')

    req = requests.get(category_link)
    src = req.text

    with open(f'data/{count}_{category_title}.html', 'w', encoding='UTF-8') as file:
        file.write(src)

    with open(f'data/{count}_{category_title}.html', encoding='UTF-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    orgs_data_dict = {}
    with open(f'data/{count}_{category_title}.csv', 'w', encoding='UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            'title',
            'adres',
            'phone_number',
            'schedule',
            'off_site',
            'mail'
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

        with open(f'data/{count}_{category_title}.csv', 'a', encoding='utf-8') as file:
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
