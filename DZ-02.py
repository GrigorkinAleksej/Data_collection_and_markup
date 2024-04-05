# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте во всех категориях:
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле

# Импорт необходимых библиотек
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse
from fake_useragent import UserAgent
import json

# Путь к странице с данным
url_baza = "http://books.toscrape.com/catalogue/"
url = "http://books.toscrape.com/catalogue/page-1.html"
ua = UserAgent()
headers = {'User-Agent': ua.chrome}
session = requests.session()

# Пустые списки, которые будут содержать соответствующие данные:
# категория, название, цена, количество товара в наличии, описание.
category = []
name = []
price = []
price_val = []
amt = []
specification = []
# Создание пустого словаря, который будет содержать все получаемые данные
output = {}

while True:
    page = session.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        next_page_link = soup.find('li', ('class', 'next'))
    except:
        next_page_link = 0
    result = soup.find_all(
        'li', ('class', 'col-xs-6 col-sm-4 col-md-3 col-lg-3'))

    # Извлечение списка относительных ссылок на товары
    url_2 = []
    for i in result:
        for link in i.find_all('div', ('class', 'image_container')):
            url_2.append(link.find('a').get('href'))

    # Объединение двух частей ссылки в абсолютный путь
    # и создание списка со ссылками на каждый товар, расположенный на странице
    url_joined = []
    for link in url_2:
        url_joined.append(urllib.parse.urljoin(url_baza, link))

    # Скрейпинг и парсинг информации о всех товарах одной страницы
    for i in url_joined:
        response = session.get(i, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Парсинг категории товара
        try:
            category.append(
                soup.find('ul', ('class', 'breadcrumb')).find_all('a')[2].text)
        except:
            category.append('')

        # Парсинг названия товара.
        try:
            name.append(
                soup.find('div', ('class', 'col-sm-6 product_main')).find('h1').text)
        except:
            name.append('')

        # Парсинг цены товара.
        try:
            p = soup.find('div', ('class', 'col-sm-6 product_main')
                          ).find('p', ('class', 'price_color')).text
            p_val = p[0]
            p = round(float(p[1:]), 2)
            price.append(p)
            price_val.append(p_val)
        except:
            price.append('')
            price_val.append('')

        # Парсинг количества товара
        try:
            amt.append(int(soup.find(
                'p', ('class', 'instock availability')).text.split('(')[1].split()[0]))
        except:
            amt.append('')

        # Парсинг описания товара
        try:
            spec = soup.find_all('p')
            specification.append(spec[3].text)
        except:
            specification.append('')

    # Записываем данные в словарь
        output = {'Название': name, 'Категория': category, 'Цена': price,
                  'Валюта': price_val, 'Количество в наличии': amt, 'Описание': specification}

    # Прерывание цикла
    if not next_page_link:
        break

    # Переход к следующей странице
    print(f"Обрабатывается страница {next_page_link.find('a')['href']}")
    url = url_baza + next_page_link.find('a')['href']

# Запись результатов в файл
with open('baza.json', 'w') as fp:
    json.dump(output, fp)
