# Импорт необходимых библиотек
import requests
import csv
import json
from lxml import html
from pprint import pprint
from fake_useragent import UserAgent

ua = UserAgent()

url = 'https://www.ebay.com'
urldop = '/b/Cycling-Computers-GPS/30108/bn_1865234'
params = {'Type': 'Bike%2520Computer', 'rt': 'nc', 'mag': 1}
# header={'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
# почему-то на мой "родной" агент сайт ничего не хочет выдавать!
header = {'User-Agent': ua.random}
# читаем страницу HTML
response = requests.get(url+urldop, headers=header, params=params)
# создаем парсинг-дерево lxml HTML из содержимого объекта ответа.
tree = html.fromstring(response.content)
items_list = []
# собираем список объектов
items = tree.xpath("//ul[@class='b-list__items_nofooter']/li")
# пробегаем по элементам списка и находим название, ссылку, цену и доп.инфу каждого элемента
for item in items:
    item_info = {}
    name = item.xpath(".//h3[@class='s-item__title']/text()")
    link = item.xpath(".//h3[@class='s-item__title']/../@href")
    price = item.xpath(".//span[@class='s-item__price']//text()")
    add_info = item.xpath(".//span[@class='NEGATIVE']/text()")
    # по возможности заносим найденные данные в словарь
    # при отсутствии данных - заносим в словарь пустое значение
    try:
        # замена немецких букв на английские - csv не хочет их почему-то писать
        a = ' '.join(name)
        a = a.replace('ö', 'o').replace(
            'ß', 's').replace('ä', 'a').replace('ü', 'u').replace('´', "'").replace('⭐', "*")
        item_info['name'] = a
        # item_info['name'] = ' '.join(name)
    except:
        item_info['name'] = ''
    try:
        item_info['link'] = ' '.join(link)
    except:
        item_info['link'] = ''
    try:
        a = ' '.join(price)
        a = a.replace(' ', '')
        item_info['price'] = a
    except:
        item_info['price'] = ''
    try:
        item_info['add_info'] = ' '.join(add_info)
    except:
        item_info['add_info'] = ''
    # добавляем словарь в список
    items_list.append(item_info)

pprint(items_list)

# раз от раза почему-то длина бывает разной
print(len(items_list))

# Структура для поиска символов "непереводимых" в файл csv
# хз, почему немецкие специальные буквы не пишутся туда
buff = []
item_info = {}
item_info['name'] = 'Что-то пошло не так!!!'
item_info['link'] = ''
item_info['price'] = ''
item_info['add_info'] = ''
buff.append(item_info)

# Запись результатов в файл csv
with open("04 velocomp.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=items_list[0].keys())
    writer.writeheader()
    try:
        writer.writerows(items_list)
    except:
        writer.writerows(buff)

# Запись результатов в файл json
with open('04 velocomp.json', 'w', encoding='utf-8') as fp:
    json.dump(items_list, fp, ensure_ascii=False)
