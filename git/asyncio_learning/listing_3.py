import socket
import selectors
import asyncio
import logging
import signal
from asyncio import AbstractEventLoop
from selectors import SelectorKey
from typing import List, Tuple, Set
from util.delay_functions import delay


def example_1():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создается сокет с IPv4 и TCP
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # указывается опция SO_REUSEADDR=1
    # для уровня сокета, чтобы повторно использовать номер порта
    server_address = ('127.0.0.1', 8000)  # выбираем нужный IP и порт для сервера
    server_socket.bind(server_address)  # привязываем его к сокету
    server_socket.listen()
    # метод listen переводит сокет в режим активного прослушивания запросов от клиентов, желающих подключиться к серверу
    connections = []
    try:
        while True:
            connection, client_address = server_socket.accept()
            # метод accept(блокирующий) необходим для ожидания запроса на подключение, он блокирует программу до
            # получения запроса, после чего возвращает объект подключения(сокет для чтения и записи клиентских данных)
            # и адрес клиента
            print(f'Получен запрос на подключение от {client_address}!')
            connections.append(connection)
            for connection in connections:
                buffer = b''
                while buffer[-2:] != b'\r\n':
                    data = connection.recv(4)  # метод recv(блокирующий) осуществляет чтение данных(в байтах) из сокета
                    if not data:
                        break
                    else:
                        print(f'Получены данные: {data}')
                        buffer += data
                print(f'Все данные: {buffer}')
                connection.send(b'Hello from server!\n')  # sendall/send(побайтно) выполняет отправку данных в сокет
    finally:
        server_socket.close()


def example_2():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.bind(server_address)
    server_socket.listen()
    server_socket.setblocking(False)  # метод setblocking необходим для перевода сокета в неблокирующий режим

    connections = []

    try:
        while True:
            try:
                connection, client_address = server_socket.accept()
                connection.setblocking(False)   # метод setblocking необходим для перевода сокета в неблокирующий режим
                print(f'Получен запрос на подключение от {client_address}!')
                connections.append(connection)
            except BlockingIOError:  # исключение BlockingIOError возникает, т.к. сокет пуст, что блокирует IO
                pass

            for connection in connections:
                try:
                    buffer = b''
                    while buffer[-2:] != b'\r\n':
                        data = connection.recv(4)
                        if not data:
                            break
                        else:
                            print(f'Получены данные: {data}')
                            buffer += data
                    print(f'Все данные: {buffer}')
                    connection.send(b'Hello from server!\n')
                except BlockingIOError:
                    pass
    finally:
        server_socket.close()


def example_3():
    selector = selectors.DefaultSelector()  # создание селектора по умолчанию

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    selector.register(fileobj=server_socket, events=selectors.EVENT_READ)
    # метод register необходим для регистрации файлового объекта(сокета) в селекторе, который будет прослушивать запросы
    # на подключение, а константа EVENT_READ означает то, что следует ожидать для данного файлового объекта(чтение)

    while True:
        events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
        # подождать 1 сек, чтобы мог выполняться другой код, при пропущенном значении timeout функция блокируется до тех
        # пор, пока не будет готов хотя бы один зарегистрированный файловый объект, при нулевом значении
        # опрос никогда не блокируется, возвращаемое значение представляет собой тройку namedtuple готовых объектов,
        # а если время истекло, то возвращается пустой список
        if len(events) == 0:  # если ничего не произошло, сообщи об этом
            print(f'Событий нет, подожду еще: events = {events}')
        for event, _ in events:
            event_socket = event.fileobj  # получить сокет, по которому произошло событие, он хранится в поле fileobj
            print(f'events = {events}, событие произошло с event_socket = {event_socket}')

            if event_socket == server_socket:  # если событие произошло с серверным сокетом, то была попытка подключения
                connection, address = server_socket.accept()
                connection.setblocking(False)
                print(f'Получен запрос на подключение от {address}')
                selector.register(connection, selectors.EVENT_READ)  # зарегистрировать клиентский сокет в селекторе
            else:  # иначе были получены данные от клиента, которые нужно принять и отправить ответ
                data = event_socket.recv(1024)
                print(f'Получены данные: {data}')
                event_socket.send(b'Hello from server!\n')


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):  # метод sock_recv ждет поступления байтов в сокет
            print('Данные получены!')
            if data == b'boom\r\n':
                raise Exception('Неожиданная ошибка сети!')
            await loop.sock_sendall(connection, b'Hello from server!\n')  # метод sock.sendall принимает сокет и данные,
            # а затем ждет, пока все данные будут отправлены
    except Exception as exp:
        logging.exception(exp)
    finally:
        connection.close()


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)  # метод sock_accept возвращает кортеж, состоящий из
        # сокета и адреса клиента
        connection.setblocking(False)
        print(f"Получен запрос на подключение от {address}")
        asyncio.create_task(echo(connection, loop))


async def example_4():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())


def cansel_tasks():
    print('Получен сигнал SIGINT!')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Снимается {len(tasks)} шт задач.')
    [task.cancel() for task in tasks]


async def example_5():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    loop.add_signal_handler(sig=signal.SIGINT, callback=cansel_tasks)  # метод add_signal_handler позволяет прослушивать
    # указанные сигналы и реагировать на них определенной функцией
    await delay(10)


echo_tasks = []


async def connection_listener(server_socket, loop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получено сообщение от {address}')
        echo_task = asyncio.create_task(echo(connection, loop))
        print(f'Создана новая задача echo_task: {echo_task}')
        echo_tasks.append(echo_task)


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 5) for task in echo_tasks]
    print(f'Текущий спискок waiters: {waiters}')
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # Здесь мы ожидаем истечения тайм-аута
            pass


async def example_6_worker(loop):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await connection_listener(server_socket, loop)


def example_6():
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(example_6_worker(loop))
    except GracefulExit:
        # print(f'exp.code: {exp.code}\nexp.args: {exp.args}\nexp: {exp}')
        loop.run_until_complete(close_echo_tasks(echo_tasks))
    finally:
        loop.close()


def main():
    example_6()


if __name__ == '__main__':
    main()
