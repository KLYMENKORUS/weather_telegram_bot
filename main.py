import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

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
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = url.json()
        pprint(data)

        city = data['name']
        current_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно не пойму что там за погода!'
        current_humidity = data['main']['humidity']
        current_pressure = data['main']['pressure']
        current_wind = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        print(f'\U0001F556 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} \U0001F556\n'
              f'Погода в городе: {city}\nТемпература: {current_weather}C° {wd}\n'
              f'Влажность: {current_humidity}%\nДавление: {current_pressure}мм.рт.ст\nВетер: {current_wind} м/c\n'
              f'Восход солнца: {sunrise_timestamp}\n'
              f'Закат солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {length_of_the_day}'
              f'\nХорошего дня!')
    except Exception as ex:
        print(ex)
        print('Проверьте названия города')


def main():
    city = input('Введите город: ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
