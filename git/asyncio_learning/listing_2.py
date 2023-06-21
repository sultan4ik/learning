import asyncio
import random
import aiohttp
from asyncio import Future

import requests

from util import delay, async_timed


async def my_couroutine() -> None:
    print('Hello, World!')


async def coroutine_add_one(number: int) -> int:
    return number + 1


def add_one(number: int) -> int:
    return number + 1


def example_2():
    function_result = add_one(1)
    coroutine_result = coroutine_add_one(1)
    print(f'Результат функции равен {function_result}, а его тип равен {type(function_result)}')
    print(f'Результат сопрограммы равен {coroutine_result}, а его тип равен {type(coroutine_result)}')


def example_3():
    result = asyncio.run(coroutine_add_one(1))
    print(result)


async def async_add_one(number: int) -> int:
    return number + 1


async def example_4():
    one_plus_one = await async_add_one(1)  # прилстановиться и ждать результата async_add_one(1)
    two_plus_one = await async_add_one(2)  # прилстановиться и ждать результата async_add_one(2)
    print(one_plus_one)
    print(two_plus_one)


async def hello_world_message() -> str:
    await delay(1)
    return 'Hello, World!'


async def example_5() -> None:
    message = await hello_world_message()
    print(message)


async def example_6() -> None:
    message = await hello_world_message()
    one_plus_one = await async_add_one(1)
    print(one_plus_one)
    print(message)


async def example_7() -> None:
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)


async def example_8() -> None:
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    await sleep_for_three
    await sleep_again
    await sleep_once_more


async def hello_every_second() -> None:
    for i in range(2):
        await asyncio.sleep(1)
        print('Пока я жду, исполняется другой код!')


async def example_9() -> None:
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_second()
    await first_delay
    await second_delay


async def example_10() -> None:
    long_task = asyncio.create_task(delay(10))
    seconds_elapsed = 0

    while not long_task.done():  # метод done возвращает True, если задача завершена, и False в обратном случае
        print('Задача не закончилась, следующая проверка через секнунду.')
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            long_task.cancel()  # метод cancel используется для остановки/отмену задачи
    try:
        await long_task
    except asyncio.CancelledError:  # в результате возникает исключение CancelledError
        print('Наша здача была снята')


async def example_11() -> None:
    delay_task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(delay_task, timeout=3)  # метод wait_for позволяет задать timeout и снять task
        print(result)
    except asyncio.TimeoutError:  # исключение TimeoutError возникает, если задача не выполнилась за timeout
        print(f'Тайм-аут! Задача была снята? {delay_task.cancelled()}')  # cancelled указывает, был ли отменен task


@async_timed()
async def example_12() -> None:
    task = asyncio.create_task(delay(10))
    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)  # метод shield защищает задачу от снятия с возникновением исключением TimeoutError по timeout
        print(result)
    except asyncio.TimeoutError:
        print('Задача заняла более 5 с, скоро она закончится!')
        result = await task
        print(result)


def example_13() -> None:
    my_future = Future()
    print(f'my_future готов? {my_future.done()}')
    my_future.set_result(44)  # метод set_result используется для учтановки значения объекта класса Future
    print(f'my_future готов? {my_future.done()}')
    print(f'Какой результат хранится в my_future? {my_future.result()}')


def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))  # создается задача, которая асинхронно установит значение future
    return future


async def set_future_value(future) -> None:
    await delay(5)
    future.set_result(42)


async def example_14():
    future = make_request()
    print(f'Будущий объект готов? {future.done()}')
    value = await future
    print(f'Будущий объект готов? {future.done()}')
    print(value)


@async_timed()
async def delay_time(delay_seconds: int) -> int:
    print(f'Засыпаю на {delay_seconds} с')
    await asyncio.sleep(delay_seconds)
    print(f'Сон в течение {delay_seconds} с закончился')
    return delay_seconds


@async_timed()
async def example_15():
    task_one = asyncio.create_task(delay(2))
    task_two = asyncio.create_task(delay(3))

    await task_one
    await task_two


@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for i in range(100000000):
        counter = counter + 1
    return counter


@async_timed()
async def example_16():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    await task_one
    await task_two


@async_timed()
async def example_17():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))
    await task_one
    await task_two
    await delay_task


async def get_three_random_pokemon():
    get_three_random_numbers = random.sample(range(1, 1010), 3)
    async with aiohttp.ClientSession() as session:
        for number in get_three_random_numbers:
            async with session.get(url=f'https://pokeapi.co/api/v2/pokemon/{number}', ssl=False) as request:
                pokemon = await request.json()
                print(f"{pokemon['id']} {pokemon['name']}")


def example_18():
    loop = asyncio.new_event_loop()  # метод new_event_loop создает цикл событий
    try:
        loop.run_until_complete(delay(3))  # метод run_untill_complete принимает сопрограмму и исполняет ее до завершения
    finally:
        loop.close()  # метод close необходми для закрытия цикла событий, чтобы освободились занятые ресурсы


def call_later():
    print('Меня вызовут в ближайшем будущем!')


async def example_19():
    loop = asyncio.get_running_loop()  # метод get_running_loop необходим для доступа к текущему циклу событий
    loop.call_soon(call_later)  # метод call_soon планирует выполнение функции на следующей итерации цикла событий
    await delay(3)


def example_20():
    loop = asyncio.new_event_loop()
    loop.slow_callback_duration = 1.250
    # с помощью метода slow_callback_duration можно задать порог времени(сек) выполнения сопрограммы,
    # при котором срабатывают предупреждения
    loop.set_debug(enabled=True)  # с помощью метода set_debug можно так же включить режим отладки
    try:
        loop.run_until_complete(example_17())
    finally:
        loop.close()


def main():
    example_20()
    # asyncio.run(example_19(), debug=True)
    # при запуске с параметром debug=True активируется отладочный режим, который отображает информационные сообщения,
    # если сопрограмма работает слишком долго(по умолчанию > 100 мс)
    # example_18()


if __name__ == '__main__':
    main()
