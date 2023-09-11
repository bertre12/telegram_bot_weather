import requests
from datetime import datetime
from pprint import pprint
from token_key import token_weather

"""
Импорт модулей:
requests - для упрощения работы с HTTP-запросами.
datetime - для обработки времени и даты.
pprint - для отформатированного представления объекта.
token_key - ссылка на токен-ключи.
"""


# Функция для запроса и вывода погоды в искомом городе.
def get_weather(city, token_weather):
    # Отображение информации на запрос и перехват исключения.
    try:
        # Переменные для отображения ответа на запрос.
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token_weather}&units=metric&lang=ru'
        )
        data = r.json()
        pprint(data)
        now = datetime.now()
        city = data['name']
        temp_weather = data['main']['temp']
        time_sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        time_sunset = datetime.fromtimestamp(data['sys']['sunset'])

        # Вывод ответа.
        print(f'Погода в данном городе - {city}\n'
              f'Текущее время - {now:%d-%m-%Y %H:%M:%S}\n'
              f'Температура - {temp_weather} C°\n'
              f'Восход солнца - {time_sunrise}\n'
              f'Заход солнца - {time_sunset}')

    # Вывод исключения.
    except Exception as ex:
        pprint(f'{ex} \n{city} - такого города нет.')


# Функция для запуска запроса.
def main():
    city = input('Напиши город для запроса погоды: ')
    get_weather(city, token_weather)


# Для запуска программы.
if __name__ == '__main__':
    main()
