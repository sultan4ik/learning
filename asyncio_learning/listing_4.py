import asyncio
import socket
import aiohttp
import logging
from util import async_timed, fetch_status
from types import TracebackType
from typing import Optional, Type


class ConnectedSocket:

    def __init__(self, server_socket):
        self._connection = None
        self._server_socket = server_socket

    async def __aenter__(self):  # вызывается при входе в блок with, ждет подкл-я клиента и возвращает это подключение
        print('Вход в контекстный менеджер, ожидание подключения')
        loop = asyncio.get_event_loop()
        connection, address = await loop.sock_accept(self._server_socket)
        self._connection = connection
        print('Подключение подтверждено')
        return self._connection

    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_val: Optional[BaseException],
                        exc_tb: Optional[TracebackType]):  # вызывается при выходе из блока with, производится очистка
        # ресурса и закрытие подключения
        print('Выход из контекстного менеджера')
        self._connection.close()
        print('Подключение закрыто')


async def example_1():
    loop = asyncio.get_event_loop()
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    # асинхронный контекстный менеджер
    async with ConnectedSocket(server_socket) as connection:  # вызов __aenter__ и начало подключения
        data = await loop.sock_recv(connection, 1024)
        print(data)
        # вызов __aexit__ и закрытие подключения


@async_timed()
async def example_2():
    async with aiohttp.ClientSession() as session:
        url = 'https://pokeapi.co/api/v2/pokemon/25'
        status = await fetch_status(session, url)
        print(f'При запросе по URL {url} был получен статус {status}')


@async_timed()
async def example_3():
    # асинхронный контекстный менеджер
    async with aiohttp.ClientSession() as session:
        urls = [f'https://pokeapi.co/api/v2/pokemon/{number}' for number in range(1, 50)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


@async_timed()
async def example_4():
    async with aiohttp.ClientSession() as session:
        urls = ['https://pokeapi.co/api/v2/pokemon/24',  'python://example.com']
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        #  по умолчанию return_exceptions=False и исключения возвращаются в точке await
        print(status_codes)


@async_timed()
async def example_5():
    async with aiohttp.ClientSession() as session:
        urls = ['https://pokeapi.co/api/v2/pokemon/24',  'python://example.com']
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests, return_exceptions=True)
        #  при return_exceptions=True исключения возвращаются в том же списке, что резульататы
        exceptions = [res for res in status_codes if isinstance(res, Exception)]
        successful_results = [res for res in status_codes if not isinstance(res, Exception)]
        print(f'Все результаты: {status_codes}')
        print(f'Завершились успешно: {successful_results}')
        print(f'Завершились с исключением: {exceptions}')


@async_timed()
async def example_6():
    async with aiohttp.ClientSession() as session:
        fetchers = [fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 10)]
        for finished_task in asyncio.as_completed(fetchers):
            # метод as_completed возвращает результаты сопрограммы по мере их выполнения
            print(await finished_task)


@async_timed()
async def example_7():
    async with aiohttp.ClientSession() as session:
        fetchers = [fetch_status(session, 'https://www.example.com', 1),
                    fetch_status(session, 'https://www.example.com', 10),
                    fetch_status(session, 'https://www.example.com', 10)]
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            # установка timeout позволяет создать исключение TimeoutError,
            # если время выполнения сопрограммы больше установленного
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('Прошел тайм-аут!')
        for task in asyncio.tasks.all_tasks():
            print(task)


@async_timed()
async def example_8():
    async with aiohttp.ClientSession() as session:
        fetchers = [asyncio.create_task(fetch_status(session, 'https://example.com', 5)),
                    asyncio.create_task(fetch_status(session, 'https://example.com'))]
        done, pending = await asyncio.wait(fetchers)
        # метод wait по умолчанию(ALL_COMPLETED) возвращает 2 множества задач, но только после их завершения
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            result = await done_task
            print(result)


@async_timed()
async def example_9():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')
        fetchers = [asyncio.create_task(good_request), asyncio.create_task(bad_request)]
        done, pending = await asyncio.wait(fetchers)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            # result = await done_task  # возбудит исключение
            if done_task.exception() is None:  # проверка на то, было ли исключение
                print(done_task.result())
            else:
                logging.error("При выполнении запроса возникло исключение", exc_info=done_task.exception())


@async_timed()
async def example_10():
    async with aiohttp.ClientSession() as session:
        fetchers = [asyncio.create_task(fetch_status(session, 'python://bad.com')),
                    asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
                    asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3))]
        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)
        # в режиме FIRST_EXCEPTION wait работает до первого исключения, задача с ошибкой помещается во множество done
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("При выполнении запроса возникло исключение", exc_info=done_task.exception())
        for pending_task in pending:
            pending_task.cancel()


@async_timed()
async def example_11():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url))]
        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_COMPLETED)
        # в режиме FIRST_COMPLETED wait работает до первого результата,
        # не важно, задача успешно заверщена или завершена с ошибкой
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            print(await done_task)


@async_timed()
async def example_12():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'
        pending = [asyncio.create_task(fetch_status(session, url)),
                   asyncio.create_task(fetch_status(session, url)),
                   asyncio.create_task(fetch_status(session, url))]
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            print(f'Число завершившихся задач: {len(done)}')
            print(f'Число ожидающих задач: {len(pending)}')
            for done_task in done:
                print(await done_task)


@async_timed()
async def example_13():
    async with aiohttp.ClientSession() as session:
        url = 'https://example.com'
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=5)),
                    asyncio.create_task(fetch_status(session, url, delay=3))]
        done, pending = await asyncio.wait(fetchers, timeout=10)
        # установливается timeout на выполнение задачи, при его сработке не возникает исключения, задача не снимается
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число ожидающих задач: {len(pending)}')
        for done_task in done:
            result = await done_task
            print(result)


async def example_14():
    async with aiohttp.ClientSession() as session:
        api_a = fetch_status(session, 'https://www.example.com')
        api_b = fetch_status(session, 'https://www.example.com', delay=2)
        #  попробуем передать сопрограммы напрямую, без оборачивания в задачи
        done, pending = await asyncio.wait([api_a, api_b], timeout=1)
        # в этом случае в wait автоматически сопрограммы обертываются задачами, при этом во множествах done и pending
        # содержат эти задачи
        for task in pending:
            if task is api_b:  # в итоге мы пытаемся сравнить задачу и сопрограмму, которые являются разными объектами
                print('API B слишком медленный, отмена')
                task.cancel()


async def example_15():
    async with aiohttp.ClientSession() as session:
        api_a = asyncio.create_task(fetch_status(session, 'https://www.example.com'))  # завернем сопрограммы в задачи
        api_b = asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=2))
        done, pending = await asyncio.wait([api_a, api_b], timeout=1)
        for task in pending:
            if task is api_b:  # сравниваем задачу с задачей
                print('API B слишком медленный, отмена')
                task.cancel()


def main():
    asyncio.run(example_13())


if __name__ == '__main__':
    main()
