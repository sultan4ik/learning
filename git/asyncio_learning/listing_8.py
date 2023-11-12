import asyncio
import sys
import os
import tty
import shutil
from asyncio import Transport, Future, AbstractEventLoop, StreamReader
from typing import Optional, AsyncGenerator, Callable, Deque, Awaitable
from util import delay
from collections import deque


class HTTPGetClientProtocol(asyncio.Protocol):

    def __init__(self, host: str, loop: AbstractEventLoop):
        self._host: str = host
        self._future: Future = loop.create_future()
        self._transport: Optional[Transport] = None
        self._response_buffer: bytes = b''

    async def get_response(self) -> Future:
        return await self._future  # ждать внутренний будущий объект, пока не будет получен ответ от сервера

    def _get_request_bytes(self) -> bytes:
        request = f"GET / HTTP/1.1\r\n" \
                  f"Connection: close\r\n" \
                  f"Host: {self._host}\r\n\r\n"
        return request.encode()

    def connection_made(self, transport: Transport):
        print(f'Создано подключение к {self._host}')
        self._transport = transport
        self._transport.write(self._get_request_bytes())  # после установки подключения использовать транспорт для
        # отправки запроса

    def data_received(self, data: bytes) -> None:
        print(f'Получены данные!')
        self._response_buffer = self._response_buffer + data  # полсе получения данных, сохранить их во внутр. буфере

    def eof_received(self) -> Optional[bool]:
        self._future.set_result(self._response_buffer.decode())  # полсе закрытия подключения завершить будующий объект,
        return False  # скопировав в него данные из буфера

    def connection_lost(self, exc: Optional[Exception]) -> None:
        if exc is None:
            print(f'Подключение закрыто без ошибок!')
        else:
            self._future.set_exception(exc)


async def make_request(host: str, port: int, loop: AbstractEventLoop) -> str:
    def protocol_factory():
        return HTTPGetClientProtocol(host, loop)

    _, protocol = await loop.create_connection(protocol_factory, host=host, port=port)
    return await protocol.get_response()


async def example_1():
    loop = asyncio.get_running_loop()
    result = await make_request('www.example.com', 80, loop)
    print(result)


async def read_until_empty(stream_reader: StreamReader) -> AsyncGenerator[str, None]:
    while response := await stream_reader.readline():  # читать и декодировать строку, пока не кончатся символы
        yield response.decode()


async def example_2():
    host: str = 'www.example.com'
    request: str = f"GET / HTTP/1.1\r\n" \
                   f"Connection: close\r\n" \
                   f"Host: {host}\r\n\r\n"
    stream_reader, stream_writer = await asyncio.open_connection('www.example.com', 80)  # возвращаются экземпляры
    #  StreamReader и StreamWriter(чтение и запись потоков данных)
    try:
        stream_writer.write(request.encode())  # записать http-запрос и опустошить буфер писателя
        await stream_writer.drain()  # данная сопрограмма блокирует выполнение, пока все находящиеся в очереди
        # данные не будут отправлены в сокет
        responses = [response async for response in read_until_empty(stream_reader)]  # читать строки и сохранять их в
        # списке
        print(''.join(responses))
    finally:
        stream_writer.close()  # закрыть писатель
        await stream_writer.wait_closed()  # и ждать завершения закрытия


async def example_3():
    while True:
        delay_time = input('Введите время сна: ')
        asyncio.create_task(delay(int(delay_time)))


async def create_stdin_reader() -> StreamReader:
    stream_reader = asyncio.StreamReader()  # создается экземпляр потокового читателя
    protocol = asyncio.StreamReaderProtocol(stream_reader)  # передача потокового читателя протоколу
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)  # подключаем канал к протоколу
    return stream_reader


async def example_4():
    stdin_reader = await create_stdin_reader()
    while True:
        delay_time = await stdin_reader.readline()
        asyncio.create_task(delay(int(delay_time)))


def save_cursor_position():
    sys.stdout.write('\0337')


def restore_cursor_position():
    sys.stdout.write('\0338')


def move_to_top_of_screen():
    sys.stdout.write('\033[H')


def delete_line():
    sys.stdout.write('\033[2K')


def clear_line():
    sys.stdout.write('\033[2K\033[0G')


def move_back_one_char():
    sys.stdout.write('\033[1D')


def move_to_bottom_of_screen() -> int:
    _, total_rows = shutil.get_terminal_size()
    input_row = total_rows - 1
    sys.stdout.write(f'\033[{input_row}E')
    return total_rows


async def read_line(stdin_reader: StreamReader) -> str:
    def erase_last_char():
        # Функция для удаления предыдущего символа из стандартного вывода
        move_back_one_char()
        sys.stdout.write(' ')
        move_back_one_char()

    delete_char = b'\x7f'
    input_buffer = deque()
    while (input_char := await stdin_reader.read(1)) != b'\n':
        if input_char == delete_char:  # Если введен символ забоя, то удалить предыдущий символ
            if len(input_buffer) > 0:
                input_buffer.pop()
                erase_last_char()
                sys.stdout.flush()
            else:
                input_buffer.append(input_char)  # Все символы, кроме забоя, добавляются в конец буфера и эхо-копируются
                sys.stdout.write(input_char.decode())
                sys.stdout.flush()
    clear_line()
    return b''.join(input_buffer).decode()


class MessageStore:
    def __init__(self, callback: Callable[[Deque], Awaitable[None]], max_size: int):
        self._deque = deque(maxlen=max_size)
        self._callback = callback

    async def append(self, item):
        self._deque.append(item)
        await self._callback(self._deque)


async def sleep(delay: int, message_store: MessageStore):
    await message_store.append(f'Начало задержки {delay}')  # добавить выходно сообщение в хранилище
    await asyncio.sleep(delay)
    await message_store.append(f'Конец задержки {delay}')


async def redraw_output(items: deque):  # обратный вызов, который перемещает курсор в начала экрана, перерисовывает
    # экран и возвращает курсор обратно
    save_cursor_position()
    move_to_top_of_screen()
    for item in items:
        delete_line()
        print(item)
    restore_cursor_position()


async def example_5():
    tty.setcbreak(sys.stdin)
    os.system('clear')

    rows = move_to_bottom_of_screen()

    messages = MessageStore(redraw_output, rows - 1)

    stdin_reader = await create_stdin_reader()

    while True:
        line = await read_line(stdin_reader)
        delay_time = int(line)
        asyncio.create_task(sleep(delay_time, messages))


def main():
    asyncio.run(example_5())


if __name__ == '__main__':
    main()
