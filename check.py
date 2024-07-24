import requests
import logging
import json

logging.basicConfig(level=logging.INFO)

REST_API_URL = input('Введите ссылку на REST API: ')


def get_api():
    try:
        response = requests.get(REST_API_URL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        logging.error(f'Ошибка получения данных REST API: {e}')
        return None
    

data = get_api()
if data:
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        logging.info('Данные успешно записаны в data.json')
else:
    logging.error('Не удалось получить данные с API')