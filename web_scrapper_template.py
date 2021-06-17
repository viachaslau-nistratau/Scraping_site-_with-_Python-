import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup
import requests
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime


# Функции для очистки данных
def to_num(price):
    """
    1. ввод значений в формате цены (к примеру 10 000 000 долларов США)
    2. нормализация значений до простого числового значения (например 10000000)
    """
    value = Decimal(sub(r'[^\d.]', '', price))
    return float(value)


def is_skipped(price):
    """
    1. определение цен, которые фактически не являются ценами (например  "POA")
    2. возврат false, если цена не указана
    """
    for i in range(len(price)):
        if price[i] != '$' and price[i] != ',' and (not price[i].isdigit()):
            return True
    return False


# базовая ссылка для парсинга рекламы
url = '{{ENTER_WEBSYTE_URL_OF_SEARCH_REQUEST_HERE}}'
map = {}
id = 0

# определить сколько страниц надо парсить
max_pages = 4
start = time.time()

for p in range(max_pages):
    cur_url = url + str(p + 1)
    print("Scrapping page: %d" % (p + 1))

    html_text = requests.get(cur_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    ads = soup.fid_all('div', class_='{{HTML CLASS TO TARGET ADD}}')

    page_nav = soup.finf_all('a', class_='{{HTML CLASS TO TARGET LINK IN NEXT BUTTON}}')

    if len(page_nav) == 0:
        print("max page number: %d" % (p))
        end = time.time()
        print(end - start)
        break

    for k in range(len(ads)):
        ad = ads[k]
        id += 1
        map[id] = {}
        # находим раздел для адреса
        address = ad.find('p', class_='{{HTML CLASS TO TARGET ADDRESS}}').text
        # находим ценовую информацию
        price = ad.find('p', class_='css-6v9gpl-Text eczcs4p0').text
        # сбрасываем, если ценовой раздел не содержит реальной цены
        if is_skipped(price):
            continue

        # находим информацию об общественном транспорте
        transport_section = ad.find('div', class_='{{HTML CLASS}}')
        transport_type = ad.find_all('span', class_='{{HTML CLASS}}')
        transport_information = transport_section.find_all('p', class_='{{HTML CLASS}})')

        # назначаем адрес
        map[id]["address"] = address
        # назначаем цену
        map[id]["price"] = price

        # создаем словари для информации об общественном транспорте
        map[id]["distance"] = []
        map[id]["station"] = []
        map[id]["transport_type"] = []

        for i in range(len(transport_information)):
            s = transport_information[i].text
            x = s.split(' km ')
            map[id]["distance"].append(float(x[0]))
            map[id]["station"].append(x[1])
            map[id]["transport_type"].append(transport_type[i]['testid'])

print("Scraping task finished")
end = time.time()
print(str(round(end - start, 2)) + 'sec')

# преобразование словаря в список списков
result = []
cur_row = 0

for id in map.keys():
    cur_price = map[cur_id]["price"]
    cur_address = map[cur_id]["address"]
    for idx in range(len(map[id]["distance"])):
        result.append([])
        result[cur_row].append(int(cur_id))
        result[cur_row].append(float(cur_price))
        result[cur_row].append(str(cur_address))
        result[cur_row].append(float(map[id]["distance"][idx]))
        result[cur_row].append(str(map[id]["station"][idx]))
        result[cur_row].append(str(map[id]["transport_type"][idx]))

        cur_row += 1

# преобразование в DataFrame
df = pd.DataFrame(result, colums = ["ad_id", "price", "address", "distance", "station", "transport_type"])

# экспорт в CSV
filename = 'test.csv'
df.to_csv(filename)
