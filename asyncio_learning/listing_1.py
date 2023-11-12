import os
import threading
import multiprocessing
import requests
import time
import concurrent.futures
import logging


def example_1():
    response = requests.get('https://www.example.com')  # Веб-запрос ограничен производительностью ввода-вывода
    items = response.headers.items()
    headers = [f'{key}: {header}' for key, header in items]  # Обработка ответа ограничена быстродействием процессора
    formatted_headers = '\n'.join(headers)  # Конкатенация строк ограничена быстродействием процессора
    with open('headers.txt', 'w') as file:
        file.write(formatted_headers)  # Запись на диск ограничена производительностью ввода-вывода


def example_2():
    print(f'Исполняется Python-процесс с идентификатором: {os.getpid()}')

    total_threads = threading.active_count()
    thread_name = threading.current_thread().name

    print(f'В данный момент Python исполняет {total_threads} поток(ов)')
    print(f'Имя текущего потока {thread_name}')


def hello_from_thread():
    print(f'Привет от потока: {threading.current_thread()}!')


def example_3():
    hello_thread = threading.Thread(target=hello_from_thread)
    hello_thread.start()

    total_threads = threading.active_count()
    threading_name = threading.current_thread().name

    print(f'В данный момент Python выполняет {total_threads} поток(ов)')
    print(f'Имя текущего потока {threading_name}')
    hello_thread.join()


def hello_from_process():
    print(f'Привет от дочернего процесса {os.getpid()}')
    time.sleep(10)


def example_4():
    hello_process = multiprocessing.Process(target=hello_from_process)
    hello_process.start()
    print(f'Привет от родительского процесса {os.getpid()}')
    hello_process.join()


def info(title):
    logging.info(title)
    logging.info('module name:', __name__)
    logging.info('parent process:', os.getppid())
    logging.info('process id:', os.getpid())
    logging.info('\n')
    time.sleep(5)


def test_function(name):
    info('function test_function')
    print('hello', name)
    print('\n')
    time.sleep(20)


def multiprocessing_test():
    info('main line')
    p = multiprocessing.Process(target=test_function, args=('Artur',))
    p1 = multiprocessing.Process(target=test_function, args=('bob',), daemon=True)
    p2 = multiprocessing.Process(target=test_function, args=('alice',), daemon=True)
    p.start()
    p1.start()
    p2.start()
    p.join()
    p1.join()
    p2.join()


def multithreading_test():
    t1 = threading.Thread(target=test_function, args=('bob',), daemon=True)
    t2 = threading.Thread(target=test_function, args=('alice',), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def print_fib(number: int) -> None:
    def fib(n: int) -> int:
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)
    print(f'fib({number}) равно {fib(number)}')


def fibs_no_threading():
    print_fib(40)
    print_fib(41)


def fibs_with_threads():
    fortieth_thread = threading.Thread(target=print_fib, args=(40,))
    forty_first_thread = threading.Thread(target=print_fib, args=(41,))
    fortieth_thread.start()
    forty_first_thread.start()
    fortieth_thread.join()
    forty_first_thread.join()


def example_5():
    start = time.time()
    fibs_no_threading()
    end = time.time()
    print(f'Время работы {end - start:.4f} с.')


def example_6():
    start = time.time()
    fibs_with_threads()
    end = time.time()
    print(f'Время работы {end - start:.4f} с.')


def read_example() -> None:
    response = requests.get('https://www.example.com')
    print(response.status_code)


def example_7():
    start = time.time()
    read_example()
    read_example()
    end = time.time()
    print(f'Синхронное выполнение заняло {end - start:.4f} с.')


def example_8():
    thread_1 = threading.Thread(target=read_example)
    thread_2 = threading.Thread(target=read_example)
    start = time.time()
    thread_1.start()
    thread_2.start()
    print('Все потоки работают')
    thread_1.join()
    thread_2.join()
    end = time.time()
    print(f'Многопоточное выполнение заняло {end - start:.4f} с.')


def thread_pool_executor_test():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_list = [executor.submit(info, name) for name in ['Artur', 'Tur', 'Ar']]
        concurrent.futures.as_completed(future_list)


def main():
    pass
    # example_3()
    # multithreading_test()
    # thread_pool_executor_test()
    # example_4()


if __name__ == '__main__':
    main()
