import time
import asyncio
import asyncpg
import functools
from util import async_timed
from asyncio.events import AbstractEventLoop
from functools import partial
from typing import List, Dict
from multiprocessing import Process, Pool, Value, Array
from concurrent.futures import ProcessPoolExecutor


def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Закончен подсчет до {count_to} за время {end - start}')
    return counter


def example_1():
    start_time = time.time()
    to_one_hundred_million = Process(target=count, args=(100000000,))  # создание процесса для выполнения функции count
    to_two_hundred_million = Process(target=count, args=(200000000,))  # создание процесса для выполнения функции count
    to_one_hundred_million.start()  # метод start запускает процесс и возвращает управление немедленно
    to_two_hundred_million.start()
    to_one_hundred_million.join()  # метод join ожидает завершения процесса и блокирует выполнение на это время
    to_two_hundred_million.join()
    end_time = time.time()
    print(f'Полное время работы {end_time - start_time}')


def say_hello(name: str) -> str:
    time.sleep(15)
    return f'Привет, {name}'


def example_2():
    with Pool() as process_pool:  # создание пула процессов с помощью контекстного менеджера, который в отличие от
        # стандартного способа с запуском и ожиданием процесса через start и join позволяет получить результат
        hi_jeff = process_pool.apply(say_hello, args=('Jeff',))  # метод apply выполненяет say_hello('Jeff')
        # в отдельном процессе и получает результат, но при этом блокирует выполнение
        hi_john = process_pool.apply(say_hello, args=('John',))
        print(hi_jeff)
        print(hi_john)


def example_3():
    with Pool(3) as process_pool:
        hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))  # метод apply_async неблокирующий и возвращает
        # сразу объект AsyncResult и начинает выполнять процесс в фоновом режиме
        hi_john = process_pool.apply_async(say_hello, args=('John',))
        hi_artur = process_pool.apply_async(say_hello, args=('Artur',))
        print(hi_jeff.get())
        print(hi_john.get())
        print(hi_artur.get())


def if_prime(number):
    if number <= 1:
        return 0
    elif number <= 3:
        return number
    elif number % 2 == 0 or number % 3 == 0:
        return 0
    i = 5
    while i**2 <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return 0
        i += 6
    return number


def sum_of_prime_numbers(process_count: int = 1, number: int = 1000000):
    with Pool(process_count) as process_pool:
        answer = sum(process_pool.map(if_prime, list(range(number))))
    print(f'answer: {answer}')


def example_4():
    with ProcessPoolExecutor(2) as process_pool:  # создание пула процессов с 2 ресурсами(по умолчанию равно числу
        # процессорных ядер,) через пул процессов ProcessPoolExecutor, который аналогичен ThreadPoolExecutor, что
        # позволяет легко переходить от процессов к потокам и обратно
        numbers = [1, 3, 5, 22, 100000000]
        for result in process_pool.map(count, numbers):  # map принимает вызываемый объект и список аргрументов, после
            # чего асинхронно выполняет объект с каждым из этих аргументов
            # существует так же метод submit, который принимает объект и возвращает объект Future - это эквивалент
            # метода Pool.apply_async
            print(result)


async def example_5():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        # создать частично применяемую функцию count c фиксированным аргументом позволяет функция partial из библиотеки
        # functools, которая из функции count(42) создает функцию count_42: call_with_42 = functools.partial(count, 42)
        # на такие ухищрения приходится идти по той причине, что метод run_in_executor не позволяет задать аргументы
        # функции и принимает только вызываемый объект
        nums = [1, 3, 5, 22, 100000000]
        calls: List[partial[int]] = [partial(count, num) for num in nums]  # сформировать все обращения к пулу
        # процессов, поместив их в список
        call_coros = []

        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))
        results = await asyncio.gather(*call_coros)  # ждать получения результатов
        for result in results:
            print(result)


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(' ')
    frequencies = {}
    for word in words:
        if word in frequencies:
            frequencies[word] = frequencies[word] + 1
        else:
            frequencies[word] = 1
    return frequencies


def merge_dictionaries_first(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


def example_6():
    lines = ["I know what I know",
             "I know that I know",
             "I don't know much",
             "They don't know much"]
    mapped_results = [map_frequency(line) for line in lines]  # выполнение функции для каждой разбитой части (mapping)
    for result in mapped_results:
        print(result)
    print(functools.reduce(merge_dictionaries_first, mapped_results))  # объединение/редукция (reducing) всех
    # промежуточных счетчиков в окончательный результат


def example_7():
    # синхронный вариант подсчета частоты слов в тексте
    freqs = {}
    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        lines = f.readlines()
        start = time.time()
        for line in lines:
            data = line.split('\t')
            word = data[0]
            count = int(data[2])
            if word in freqs:
                freqs[word] = freqs[word] + count
            else:
                freqs[word] = count
        end = time.time()
        print(f'{end - start:.4f}')


def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]


def map_frequencies_first(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)
    return counter


def merge_dictionaries_second(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    return merged


async def example_8(partition_size: int):
    # асинхронный вариант подсчета частоты слов в тексте методом MapReduce с использованием многопроцессорности
    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        with ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies_first, chunk)))
            intermediate_results = await asyncio.gather(*tasks)
            final_result = functools.reduce(merge_dictionaries_second, intermediate_results)
            print(f"Aardvark встречается {final_result['Aardvark']} раз.")
            end = time.time()
            print(f'Время MapReduce: {(end - start):.4f} секунд')


def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


def example_9():
    integer = Value('i', 0)  # объявление разделяемого целого числа
    integer_array = Array('i', [0, 0])  # объявление разделяемого массива
    procs = [Process(target=increment_value, args=(integer,)),
             Process(target=increment_array, args=(integer_array,))]
    [p.start() for p in procs]
    [p.join() for p in procs]
    print(integer.value)
    print(integer_array[:])


def example_10():
    # демонстрация состояния гонки
    for _ in range(100):
        integer = Value('i', 0)  # объявление разделяемой переменной int
        procs = [Process(target=increment_value, args=(integer,)), Process(target=increment_value, args=(integer,))]
        [p.start() for p in procs]
        [p.join() for p in procs]
        print(integer.value)
        assert(integer.value == 2)


def increment_value_with_lock(shared_int: Value):
    shared_int.get_lock().acquire()  # происходит захват блокировки разделяемых данных
    shared_int.value = shared_int.value + 1
    shared_int.get_lock().release()  # происходит освобождение разделяемых данных
    # with shared_int.get_lock():  # блокировка является контекстным менеджером, лучше использовать такой вариант
    #     shared_int.value = shared_int.value + 1


def example_11():
    # устранение состояния гонки с помощью блокировки
    for _ in range(100):
        integer = Value('i', 0)
        procs = [Process(target=increment_value_with_lock, args=(integer,)),
                 Process(target=increment_value_with_lock, args=(integer,))]
        [p.start() for p in procs]
        [p.join() for p in procs]
        print(integer.value)
        assert(integer.value == 4)


shared_counter: Value


def first_init(first_counter: Value):
    global shared_counter
    shared_counter = first_counter


def increment():
    with shared_counter.get_lock():
        shared_counter.value += 1


async def example_12():
    #  в случае, когда используется пул процессов, разделяемые переменные необходимо заносить в глобальную переменную
    counter = Value('d', 0)
    with ProcessPoolExecutor(initializer=first_init,
                             initargs=(counter,)) as pool:  # функция init принимает объявленный нами Value и
        # инициализирует shared_counter этим значением, передаем ее в качестве инициализатора пула процессов, а это
        # значит, что в каждом процессе можно будет ссылаться на разделяемую память, выделенную родительским процессом
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        print(counter.value)


map_progress: Value


def second_init(progress: Value):
    global map_progress
    map_progress = progress


def map_frequencies_second(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)
    with map_progress.get_lock():
        map_progress.value += 1
    return counter


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f'Завершено операций отображения: {map_progress.value}/{total_partitions}')
        await asyncio.sleep(1)


async def example_13(partition_size: int):
    global map_progress
    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value('i', 0)
        with ProcessPoolExecutor(max_workers=2, initializer=second_init, initargs=(map_progress,), ) as pool:
            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))
            for chunk in partition(contents, partition_size):
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies_second, chunk)))
            counters = await asyncio.gather(*tasks)
            await reporter
            final_result = functools.reduce(merge_dictionaries_second, counters)
            print(f"Aardvark встречается {final_result['Aardvark']} раз.")


product_query = """
SELECT
p.product_id,
p.product_name,
p.brand_id,
s.sku_id,
pc.product_color_name,
ps.product_size_name
FROM product as p
JOIN sku as s on s.product_id = p.product_id
JOIN product_color as pc on pc.product_color_id = s.product_color_id
JOIN product_size as ps on ps.product_size_id = s.product_size_id
WHERE p.product_id = 100"""


async def query_product(pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


def run_in_new_loop(num_queries: int) -> List[Dict]:
    async def run_queries():
        async with asyncpg.create_pool(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       password='password',
                                       database='postgres',
                                       min_size=6,
                                       max_size=6) as pool:
            return await query_products_concurrently(pool, num_queries)
    results = [dict(result) for result in asyncio.run(run_queries())]
    return results


@async_timed()
async def example_14():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = [loop.run_in_executor(pool, run_in_new_loop, 10000) for _ in range(5)]
    all_results = await asyncio.gather(*tasks)
    total_queries = sum([len(result) for result in all_results])
    print(f'Извлечено товаров из базы данных: {total_queries}.')


def main():
    asyncio.run(example_14())


if __name__ == '__main__':
    main()
