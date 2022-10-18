import requests
import datetime
from config import telegram_token_bot, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Bot(token=telegram_token_bot)
dispatcher_bot = Dispatcher(bot)


@dispatcher_bot.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! \U0001F44B\n'
                        'Напиши мне название своего населенного пункта и я пришлю погоду!')


@dispatcher_bot.message_handler()
async def get_weather(message: types.Message):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U0001F327',
        'Drizzle': 'Дождь \U0001F327',
        'Thunderstorm': 'Гроза \U0001F329',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }
    try:
        url = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = url.json()
        city = data['name']
        current_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно не пойму что там за погода!'
        current_humidity = data['main']['humidity']
        current_wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        await message.reply(f'\U0001F556 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                            f'\U000026C5 Погода в городе: {city}\n'
                            f'\U0001F321 Температура: {current_weather}C° {wd}\n'
                            f'\U0001F4A7 Влажность: {current_humidity}%'
                            f'\U0001F32C Ветер: {current_wind} м/c\n'
                            f'\U0001F305 Восход солнца: {sunrise_timestamp}\n'
                            f'\U0001F307 Закат солнца: {sunset_timestamp}\n'
                            f'\U0001F567 Продолжительность дня: {length_of_the_day}'
                            f'\nХорошего дня! \U0001F609')
    except:
        await message.reply('\U0000274C Проверьте названия города \U0000274C')


@dispatcher_bot.callback_query_handler(lambda c: c.data == 'butt_id')
async def get_weather_three(call: types.callback_query):
    await bot.answer_callback_query(call.id)


if __name__ == '__main__':
    executor.start_polling(dispatcher_bot)
