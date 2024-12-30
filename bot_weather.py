import requests
from datetime import datetime
import pytz
from token_key import token_weather, token_bot
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

"""
Импорт модулей:
requests - для упрощения работы с HTTP-запросами.
datetime - для обработки времени и даты.
token_key - ссылка на токен-ключи.
aiogram - для работы бота.
pytz - для корректного отображения временной зоны.
"""

# Создание объект бота.
bot = Bot(token=token_bot)

# Создание диспетчера для управления ботом.
dp = Dispatcher(bot)


# Функция для старта бота.
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        'Привет, напиши название города и получишь сводку о погоде на сегодня 😊')


# Функция для запроса и вывода погоды в искомом городе.
@dp.message_handler()
async def get_weather(message: types.Message):
    # Отображение информации на запрос и перехват исключения.
    try:
        # Переменные для отображения ответа на запрос.
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token_weather}&units=metric&lang=ru'
        )
        data = r.json()
        now = datetime.now()
        city = data['name']
        temp_weather = data['main']['temp']
        time_sunrise = datetime.fromtimestamp(data['sys']['sunrise'])
        time_sunset = datetime.fromtimestamp(data['sys']['sunset'])

        # Устанавливаем временную зону.
        timezone = pytz.timezone('Europe/Minsk')  # Устанавливаем временную
        # зону на Минск.
        now = datetime.now(timezone)  # Получаем текущее время в нужной
        # временной зоне.
        time_sunrise = time_sunrise.astimezone(timezone)  # Приводим к нужной
        # временной зоне.
        time_sunset = time_sunset.astimezone(timezone)  # Приводим к нужной
        # временной зоне.

        # Вывод ответа.
        await message.reply(f'Погода в данном городе - {city}\n'
                            f'Текущее время - {now:%d-%m-%Y %H:%M:%S}\n'
                            f'Температура - {temp_weather} C°\n'
                            f'Восход солнца - {time_sunrise:%d-%m-%Y %H:%M:%S}\n'
                            f'Заход солнца - {time_sunset:%d-%m-%Y %H:%M:%S}')

    # Вывод исключения.
    except:
        await message.reply(f'{message.text} - такого города нет😕.')


# Для запуска бота.
if __name__ == '__main__':
    executor.start_polling(dp)
