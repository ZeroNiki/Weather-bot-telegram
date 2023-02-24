import requests
import datetime
from config import TOKEN, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Hi! Write to me if you want to know the weather")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear" : "Clear \U00002600",
        "Clouds" : "Clouds \U00002601",
        "Rain" : "Rain \U00002614",
        "Drizzle" : "Rain \U00002614",
        "Thunderstorm" : "Thunderstorm \U000026A1",
        "Snow" : "Snow \U0001F328",
        "Mist" : "Mist \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_discription = data["weather"][0]["main"]
        if weather_discription in code_to_smile:
            wd = code_to_smile[weather_discription]
        else:
            wd = "Look out the window, I don't understand what is happening"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Weather in the city: {city}\nTemp: {cur_weather}С° {wd}"
              f"\nHumidity: {humidity}%\nPressure: {pressure}mmHg\nWind: {wind}m/s"
              f"\nSunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nDuration of the day: {length_of_the_day}"
              "\n***Good day!***")

    except:
        await message.reply("\U00002620 Check the name of the city \U00002620")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)