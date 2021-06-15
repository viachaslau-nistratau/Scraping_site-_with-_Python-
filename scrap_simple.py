from bs4 import BeautifulSoup
import requests

import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd

# поиск в определённой зоне
url = 'https://www.website.com/london/page_size=25&q=london&pn=1'

# делаем запрос и получаем html
html_text = requests.get(url).text

# используем парсер lxml
soup = BeautifulSoup(html_text, 'lxml')
# Переменная soup содержит полный HTML-код страницы с результатами поиска.

# находим одно объявление
ad = soup.find('div', class_ = 'css-ad-wrapper-123456')

# находим цену
#vprice = ad.find('p', class_ = 'css-aaabbbccc').txt
# Использование .text в конце метода find() позволяет возвращать
# только обычный текст, как показано в браузере.
# Без .text он вернет весь исходный код строки HTML, на которую ссылается класс

# Чтобы получить ценники для всех объявлений,
# применяем метод find.all() вместо find()
#  = ad.find_all('p', class_ = 'css-ad-wrapper-123456')
# Переменная ads теперь содержит HTML-код для каждого объявления на первой
# странице результатов в виде списка списков.

# Чтобы получить все ценники, используем словарь для сбора данных:
map = {}
id = 0 
# получаем все элементы
ads = ad.find_all('p', class_ = 'css-ad-wrapper-123456')

for i in range(len(ads)):
    ad = ads[i]
    id += 1
    map[id] = {}

    # находим цену
    price = ad.find('p', class_ = 'css-aaabbbccc').text
    # находим адрес
    address = ad.find('p', class_ = 'css-address-123456').text
    map[id]["address"] = address
    map[id]["price"] = price

# примечание: использование идентификатора позволяет находить объявления в словаре:
# {'id': '1',
#  'address': 'Holland Road, London SW17',
#  'price': '550.000'
#  }

"""
Получение точек данных со всех страниц
Обычно результаты поиска либо разбиваются на страницы, 
либо бесконечно прокручиваются вниз.
"""

"""
Вариант 1. Веб-сайт с пагинацией

URL-адреса, полученные в результате поискового запроса, 
обычно содержат информацию о текущем номере страницы.
Окончание URL-адреса относится к номеру страницы результатов.
Важное примечание: номер страницы в URL-адресе обычно становится видимым 
со второй страницы. Использование базового URL-адреса с дополнительным 
фрагментом &pn=1 для вызова первой страницы по-прежнему будет работать 
(в большинстве случаев).
"""
# Применение одного цикла for-loop поверх другого
# позволяет нам перебирать страницы результатов

url = 'https://www.website.com/london/page_size=25&q=london&pn='

map = {}
id = 0

# максимальное количество страниц
max_pages = 15

for p in range(max_pages):
    cur_url = url + str(p + 1)
    print("Скрапинг страницы №: %d" % (p + 1))
    html_text = requests.get(cur_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    ads = soup.find_all('div', class_ = 'css-add-wrapper-123456')

    for i in range(len(ads)):
        ad = ads[i]
        id += 1
        map[id] = {}

        price = ad.find('p', class_ = 'css-aaabbbccc').text
        address = ad.find('p', class_ = 'css-address-123456').text
        map[id]["address"] = address
        map[id]["price"] = price

    # как определить последнюю страницу результатов? В большинстве случаев
    # после достижения последней страницы, любой запрос с большим числом,
    # чем фактическое число последней страницы, приведет нас обратно на первую.
    # Следовательно, использование очень большого числа для ожидания завершения
    # сценария не работает. Через некоторое время он начнет собирать повторяющиеся
    # значения.
    # Чтобы решить эту проблему, будем проверять, есть ли на странице
    # кнопка с такой ссылкой:

url = 'https://www.website.com/london/page_size=25&q=london&pn='
map = {}
id = 0

# используем очень большое число
max_pages = 9999

for p in range(max_pages):
    cur_url = url + str(p + 1)
    print("Скрапинг страницы №: %d" % (p + 1))
    html_text = requests.get(cur_url).text
    soup = BeautifulSoup(html_text, 'lxml')
    ads = soup.find_all('div', class_ = 'css-add-wrapper-123456')

    # ищем ссылку в кнопке
    page_nav = soup.find_all('a', class_ = 'css-button-123456')
    if len(page_nav) == 0:
        print("Максимальный номер страницы: %d" % (p))
        break
    (.....)

"""
Вариант 2. Сайт с бесконечным скроллом
В таком случае HTML скрапер не сработает.
"""
# Устранение несогласованности данных
# Если нам нужно избавиться от ненужных данных в самом начале скрапинга на Python,
# можно использовать обходной метод.
# Функция для определения аномалий

def is_skipped(price):
    """
    Определение цен, которые не являются ценами
    (например "Цена по запросу")
    """
    for i in range(len(price)):
        if price[i] != "$" and price[i] != ',' and (not price[i].isdigit()):
            return True
    return False
# И применить его при сборе данных:
(....)
for i in range(len(ads)):
    ad = ads[i]
    id += 1
    map[id] = {}

    price = ad.find('p', class_ = 'css-aaabbbccc').text
    # пропускаем объявление без корректной цены
    if is_skipped(price):
        continue
    map[id]["price"] = price

# Форматирование данных на лету
# цена хранится в строке вместе с запятыми с символом валюты.
# можно исправить это ещё на этапе скрапинга:

def to_num(price):
    value = Decimal(sub(r'[^\d.]', '', price))
    return float(value)

# Используем эту функцию:

(....)
for i in range(len(ads)):
    ad = ads[i]
    id += 1
    map[id] = {}

    price = ad.find('p', class_ = 'css-aaabbbccc').text
    if is_dropped(price):
        continue
        map[id]["price"] = to_num(price)
        (....)

# Получение вложенных данных
# Информация об общественном транспорте имеет вложенную структуру.
# Нам потребуются данные о расстоянии, названии станции и типе транспорта.
# Отбор информации по правилам
# Каждый кусочек данных представлен в виде: число миль, название станции.
# Используем слово «миль» в качестве разделителя.

map[id]["distance"] = []
map[id]["station"] = []
transport = ad.find_all('div', class_ = 'css-transport-123')
for i in range(len(transport)):
    s = transport[i].text
    x = s.split(' miles ')
    map[id]["distance"].append(float(x[0]))
    map[id]["station"].append(x[1])

# Первоначально переменная transport хранит два списка в списке, поскольку есть
# две строки информации об общественном транспорте (например,
# “0,3 мили Слоун-сквер”, “0,5 мили Южный Кенсингтон”).
# Мы перебираем эти списки, используя len транспорта в качестве значений индекса,
# и разделяем каждую строку на две переменные: расстояние и станцию.
# Поиск дополнительных HTML атрибутов для визуальной информации
# В коде страницы мы можем найти атрибут testid, который указывает на
# тип общественного транспорта. Он не отображается в браузере,
# но отвечает за изображение, которое отображается на странице.
# Для получения этих данных нам нужно использовать класс css-StyledIcon:

map[id]["distance"] = []
map[id]["station"] = []
map[id]["transport_type"] = []
transport = ad.find_all('div', class_ = 'css-transport-123')
type = ad.find_all('span', class_ = 'css-StyledIcon')
for i in range(len(transport)):
       s = transport[i].text
       x = s.split(' miles ')
       map[id]["distance"].append(float(x[0]))
       map[id]["station"].append(x[1])
       map[id]["transport_type"].append(type[i]['testid'])

# Преобразование в датафрейм и экспорт в CSV
# Когда скрапинг выполнен, все извлеченные данные доступны в словаре словарей.

# Преобразуем словарь в список списков, чтобы избавиться от вложенности

result = []
cur_row = 0
for idx in range(len(map[1]["distance"])):
    result.append([])

    result[cur_row].append(str(map[1]["uuid"]))
    result[cur_row].append(str(map[1]["price"]))
    result[cur_row].append(str(map[1]["address"]))
    result[cur_row].append(str(map[1]["distance"][idx]))
    result[cur_row].append(str(map[1]["station"][idx]))
    result[cur_row].append(str(map[1]["transport_type"][idx]))

    cur_row += 1

# Создаём датафрейм

df = pd.DataFrame(
    result, columns = ["ad_id", "price", "address",
                       "distance", "station", "transport_type"
                       ]
)
# можем экспортировать датафрейм в CSV:
filename = 'test.csv'
df.to_csv(filename)

# Преобразование всех объявлений в датафрейм:
result = []
cur_row = 0
for id in map.keys():
    cur_price = map[id]["price"]
    cur_address = map[id]["address"]
    for idx in range(len(map[id]["distance"])):
        result.append([])
        result[cur_row].append(int(cur_id))
        result[cur_row].append(float(cur_price))
        result[cur_row].append(str(cur_address))
        result[cur_row].append(float(map[id]["distance"][idx]))
        result[cur_row].append(str(map[id]["station"][idx]))
        result[cur_row].append(str(map[id]["transport_type"][idx]))
        cur_row += 1
# преобразование в датафрейм
df = pd.DataFrame(result, columns = ["ad_id", "price","address",
                                     "distance", "station", "transport_type"
                                     ]
)
# экспорт в csv
filename = 'test.csv'
df.to_csv(filename)







