import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

    # Учетные данные API
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    token = os.getenv('token')

    # Конечная точка API
    endpoint = "https://api.foursquare.com/v3/places/search"

    # Определение параметров для запроса API
    city = input("Введите название города: ")
    category = input("Введите категорию заведения: ")
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "near": city,
        "query": category
    }
    headers = {
        "Accept": "application/json",
        "Authorization": token
    }

    # Отправка запроса API и получение ответа
    response = requests.get(endpoint, params=params, headers=headers)

    # Проверка успешности запроса API
    if response.status_code == 200:
        print("Успешный запрос API!")
        data = json.loads(response.text)
        venues = data["results"]
        for venue in venues:
            print("Название:", venue["name"])
            print("Адрес:", venue["location"]["formatted_address"])
            print("\n")
    else:
        print("Запрос API завершился неудачей с кодом состояния:",
              response.status_code)
        print(response.text)
else:
    print('что-то пошло не так')  # не буду пока обрабатывать этот вариант
