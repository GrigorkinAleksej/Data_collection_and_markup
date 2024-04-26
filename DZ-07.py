# Импорт необходимых библиотек
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


# Установка веб-драйвера
driver = webdriver.Chrome()

# Переход на веб-сайт ТВ-программы
# driver.get("https://tv.starhit.ru/chelyabinsk")
# driver.get("https://tv.starhit.ru/chelyabinsk?category=movie")
driver.get("https://tv.starhit.ru/chelyabinsk?date=2024-05-01&category=sport")

# Подтверждение города
city = driver.find_element(
    By.XPATH, '//span[@class="_tooltipBtnYes_16670_15"]')
city.click()

# Организация прокрутки страницы до конца вниз
wait = WebDriverWait(driver, 10)
while True:
    channels = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@class="_channel_1a1ke_1"]')))
    count = len(channels)
    print(count)
    driver.execute_script('window.scrollBy(0,10000)')
    time.sleep(1)
    channels = driver.find_elements(
        By.XPATH, '//div[@class="_channel_1a1ke_1"]')
    if len(channels) == count:
        break
print(count)

# Без прокрутки вверх почему-то не раскрываются все программы на первых двух каналах
driver.execute_script('window.scrollTo(0, 0)')

# Перебор всех каналов
full_programm = {}
num = 0
for channel in channels:

    # Раскрытие списка всех передач канала
    try:
        button = channel.find_element(
            By.XPATH, './/button[@class="d-flex justify-content-c align-items-c w-100"]')
        button.click()
    except:
        pass

    # Название канала
    num += 1
    name = channel.find_element(
        By.XPATH, './/div[@class="_title_lpcs3_12"]').text
    print(num, name)

    # Формирование списка передач канала
    items = channel.find_elements(
        By.XPATH, './/a[contains(@class, "_uiLink_11hrn_1 text-style-body-caption-2")]')

    # Перебор всех передач канала
    programm = {}
    for item in items:
        time_item = item.find_element(
            By.XPATH, './/div[@class="_itemTime_jkbng_18"]').text
        text_item = item.find_element(
            By.XPATH, './/span[@class="_programmeTitle_jkbng_23"]').text

        # Наполнение словаря передач канала
        programm[time_item] = text_item

    # Наполнение словаря каналов
    full_programm[name] = programm

# Запись данных в файл JSON
# file_name = 'tv_programm.json'
# file_name = 'kino_programm.json'
file_name = 'sport_programm_01_05.json'
with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(full_programm, f, ensure_ascii=False, indent=4)

driver.close()
