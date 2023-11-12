import asyncio
import time
from aiohttp import ClientSession


async def get_weather(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            print(f'{city}: {weather_json["weather"][0]["main"]}')


async def get_weather_with_return(city):
    async with ClientSession() as session:
        url = f'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

        async with session.get(url=url, params=params) as response:
            weather_json = await response.json()
            return f'{city}: {weather_json["weather"][0]["main"]}'


async def main(cities_):
    tasks = []
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather(city)))
    for task in tasks:
        await task


async def main_with_return(cities_):
    # gather используется в том случае, когда асинхронная функция возвращает что-то
    tasks = []
    for city in cities_:
        tasks.append(asyncio.create_task(get_weather_with_return(city)))
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

cities = ['Ufa', 'Istanbul', 'Tokyo', 'Isyangulovo']

start_time = time.time()

asyncio.run(main_with_return(cities))

print(f'{round(time.time() - start_time, 3)} sec')