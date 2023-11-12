import functools
import asyncio
import os
import socket
import time
import requests
import tkinter
import hashlib
import string
import random
import numpy as np
from aiohttp import ClientSession
from tkinter import Tk, Label, Entry, ttk
from typing import List, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, Future
from util import async_timed
from threading import Lock, Thread, RLock
from asyncio import AbstractEventLoop
from queue import Queue


def echo(client: socket):
    while True:
        data = client.recv(2048)
        print(f'Получно {data}, отправляю!')
        client.sendall(data)


def example_1():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        while True:
            connection, _ = server.accept()  # метод блокирующий, т.е. блокируется в ожидании подключения клиентов
            thread = Thread(target=echo, args=(connection,))  # как только подключился клиент, создать поток для
            # выполнения функции echo
            thread.start()  # начать выполнение потока


class ClientEchoThread(Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        try:
            while True:
                data = self.client.recv(2048)
                if not data:  # если нет данных, то возбудить исключение(подключение закрыто клиентом или
                    # остановлено сервером)
                    raise BrokenPipeError('Подключение закрыто!')
                print(f'Получено {data}, отправляю!')
                self.client.sendall(data)
        except OSError as exp:  # выход из метода run в случае исключения, завершение работы потока
            print(f'Поток прерван исключением {exp}, производится остановка!')

    def close(self):
        if self.is_alive():  # разомкнуть подключение, если поток еще активен
            self.client.sendall(bytes('Останавливаюсь!', encoding='utf-8'))
            self.client.shutdown(socket.SHUT_RDWR)  # разомкнуть подключение клиента, остановив чтение и запись


def example_2():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 8000))
        server.listen()
        connection_threads = []
        try:
            while True:
                connection, addr = server.accept()
                thread = ClientEchoThread(connection)
                connection_threads.append(thread)
                thread.start()
        except KeyboardInterrupt:
            print('Останавливаюсь!')
            [thread.close() for thread in connection_threads]  # метод close для созданных потоков, чтобы разомкнуть все
            # все клиентские подключения в случае прерывания с клавиатуры


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


def example_3():
    start = time.time()

    with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4)) as pool:
        urls = ['https://www.example.com' for _ in range(1000)]
        results = pool.map(get_status_code, urls)
        for result in results:
            print(result)

    end = time.time()
    print(f'Выполнение запросов завершено за {end-start:.4f} с')


@async_timed()
async def example_4():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        urls = ['https://www.example.com' for _ in range(1000)]
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code, url)) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)


@async_timed()
async def example_5():
    urls = ['https:// www.example.com' for _ in range(1000)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]  # asyncio.to_thread передает работу исполнителю
    # пула потоков по умолчанию
    results = await asyncio.gather(*tasks)
    print(results)


counter_lock = Lock()
counter: int = 0


def get_status_code_with_global_counter(url: str) -> int:
    global counter
    response = requests.get(url)
    with counter_lock:
        counter = counter + 1
    return response.status_code


async def reporter(request_count: int):
    while counter < request_count:
        print(f'Завершено запросов: {counter}/{request_count}')
        await asyncio.sleep(.5)


@async_timed()
async def example_6():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        request_count = 200
        urls = ['https://www.example.com' for _ in range(request_count)]
        reporter_task = asyncio.create_task(reporter(request_count))
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code_with_global_counter, url)) for url in urls]
        results = await asyncio.gather(*tasks)
        await reporter_task
        print(results)


# list_lock = Lock()
list_lock = RLock()


def sum_list(int_list: List[int]) -> int:
    # данный пример показывает, что доступ к разделяемой переменной одного и того же потока приводит к завису, данную
    # проблему устраняют реентерабельные блокировки(RLock), которые допускают неоднократный захват из одного потока
    print('Ожидание блокировки...')
    with list_lock:
        print('Блокировка захвачена.')
        if len(int_list) == 0:
            print('Суммирование завершено.')
            return 0
        else:
            head, *tail = int_list
            print('Суммируется остаток списка.')
            return head + sum_list(tail)


def example_7():
    thread = Thread(target=sum_list, args=([1, 2, 3, 4],))
    thread.start()
    thread.join()


lock_a = Lock()
lock_b = Lock()


def a():
    with lock_a:  # захватить блкоировки А
        print('Захвачена блокировка a из метода a!')
        # time.sleep(1)  # ждать 1 секунду для подходящего условия взаимоблокировки
        with lock_b:  # захватить блокировку В
            print('Захвачены обе блокировки из метода a!')


def b():
    with lock_b:  # захватить блокировку В
        print('Захвачена блокировка b из метода b!')
        with lock_a:  # захватить блокировку A
            print('Захвачены обе блокировки из метода b!')


def example_8():
    # пример с взаимоблокировкой между двумя процессами - deadlock
    thread_1 = Thread(target=a)
    thread_2 = Thread(target=b)
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()


def say_hello():
    print('Привет!')
    time.sleep(10)


def example_9():
    window = tkinter.Tk()
    window.title('Hello world app')
    window.geometry('200x100')
    hello_button = ttk.Button(window, text='Say hello', command=say_hello)
    hello_button.pack()
    window.mainloop()


class StressTest:

    def __init__(self,
                 loop: AbstractEventLoop,
                 url: str,
                 total_requests: int,
                 callback: Callable[[int, int], None]):
        self._completed_requests: int = 0
        self._load_test_future: Optional[Future] = None
        self._loop = loop
        self._url = url
        self._total_requests = total_requests
        self._callback = callback
        self._refresh_rate = total_requests // 100

    def start(self):
        future = asyncio.run_coroutine_threadsafe(self._make_requests(),
                                                  self._loop)
        self._load_test_future = future

    def cancel(self):
        if self._load_test_future:
            self._loop.call_soon_threadsafe(self._load_test_future.cancel)

    async def _get_url(self, session: ClientSession, url: str):
        try:
            await session.get(url)
        except Exception as e:
            print(e)
        self._completed_requests += 1
        if self._completed_requests % self._refresh_rate == 0 \
                or self._completed_requests == self._total_requests:
            self._callback(self._completed_requests, self._total_requests)

    async def _make_requests(self):
        async with ClientSession() as session:
            reqs = [self._get_url(session, self._url) for _ in
                    range(self._total_requests)]
        await asyncio.gather(*reqs)


class LoadTester(Tk):

    def __init__(self, loop, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self._queue = Queue()
        self._refresh_ms = 25

        self._loop = loop
        self._load_test: Optional[StressTest] = None
        self.title('URL Requester')

        self._url_label = Label(self, text="URL:")
        self._url_label.grid(column=0, row=0)

        self._url_field = Entry(self, width=10)
        self._url_field.grid(column=1, row=0)

        self._request_label = Label(self, text="Number of requests:")
        self._request_label.grid(column=0, row=1)

        self._request_field = Entry(self, width=10)
        self._request_field.grid(column=1, row=1)

        self._submit = ttk.Button(self, text="Submit", command=self._start)
        self._submit.grid(column=2, row=1)

        self._pb_label = Label(self, text="Progress:")
        self._pb_label.grid(column=0, row=3)

        self._pb = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self._pb.grid(column=1, row=3, columnspan=2)

    def _update_bar(self, pct: int):
        if pct == 100:
            self._load_test = None
            self._submit['text'] = 'Submit'
        else:
            self._pb['value'] = pct
            self.after(self._refresh_ms, self._poll_queue)

    def _queue_update(self, completed_requests: int, total_requests: int):
        self._queue.put(int(completed_requests/total_requests * 100))

    def _poll_queue(self):
        if not self._queue.empty():
            percent_complete = self._queue.get()
            self._update_bar(percent_complete)
        else:
            if self._load_test:
                self.after(self._refresh_ms, self._poll_queue)

    def _start(self):
        if self._load_test is None:
            self._submit['text'] = 'Cancel'
            test = StressTest(self._loop,
                              self._url_field.get(),
                              int(self._request_field.get()),
                              self._queue_update)
            self.after(self._refresh_ms, self._poll_queue)
            test.start()
            self._load_test = test
        else:
            self._load_test.cancel()
            self._load_test = None
            self._submit['text'] = 'Submit'


class ThreadedEventLoop(Thread):

    def __init__(self, loop: AbstractEventLoop):
        super().__init__()
        self._loop = loop
        self.daemon = True

    def run(self):
        self._loop.run_forever()


def example_10():
    loop = asyncio.new_event_loop()
    asyncio_thread = ThreadedEventLoop(loop)
    asyncio_thread.start()
    app = LoadTester(loop)
    app.mainloop()


def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in
                    range(length))


passwords = [random_password(10) for _ in range(10000)]


def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


def example_11():
    start = time.time()

    for password in passwords:
        hash(password)

    end = time.time()
    print(end - start)


@async_timed()
async def example_12():
    loop = asyncio.get_running_loop()
    tasks = []
    with ThreadPoolExecutor() as pool:
        for password in passwords:
            tasks.append(loop.run_in_executor(pool, functools.partial(hash, password)))
    await asyncio.gather(*tasks)


data_points = 1_000_000_000
rows = 50
columns = int(data_points / rows)
matrix = np.arange(data_points).reshape(rows, columns)


def example_13():
    start = time.time()
    res = np.mean(matrix, axis=1)
    end = time.time()
    print(end - start)


def mean_for_row(arr, row):
    return np.mean(arr[row])


@async_timed()
async def example_14():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        tasks = []
        for i in range(rows):
            mean = functools.partial(mean_for_row, matrix, i)
            tasks.append(loop.run_in_executor(pool, mean))
        results = asyncio.gather(*tasks)


def main():
    asyncio.run(example_14())
    # example_13()


if __name__ == '__main__':
    main()
