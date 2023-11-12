import asyncpg
import asyncio
import logging
from util import async_timed, delay
from asyncpg import Record
from random import sample, randint
from typing import List, Tuple, Union
from asyncpg.transaction import Transaction


CREATE_BRAND_TABLE = """
CREATE TABLE IF NOT EXISTS brand(
brand_id SERIAL PRIMARY KEY,
brand_name TEXT NOT NULL
);"""
CREATE_PRODUCT_TABLE = """
CREATE TABLE IF NOT EXISTS product(
product_id SERIAL PRIMARY KEY,
product_name TEXT NOT NULL,
brand_id INT NOT NULL,
FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
);"""
CREATE_PRODUCT_COLOR_TABLE = """
CREATE TABLE IF NOT EXISTS product_color(
product_color_id SERIAL PRIMARY KEY,
product_color_name TEXT NOT NULL
);"""
CREATE_PRODUCT_SIZE_TABLE = """
CREATE TABLE IF NOT EXISTS product_size(
product_size_id SERIAL PRIMARY KEY,
product_size_name TEXT NOT NULL
);"""
CREATE_SKU_TABLE = """
CREATE TABLE IF NOT EXISTS sku(
sku_id SERIAL PRIMARY KEY,
product_id INT NOT NULL,
product_size_id INT NOT NULL,
product_color_id INT NOT NULL,
FOREIGN KEY (product_id)
REFERENCES product(product_id),
FOREIGN KEY (product_size_id)
REFERENCES product_size(product_size_id),
FOREIGN KEY (product_color_id)
REFERENCES product_color(product_color_id)
);"""
COLOR_INSERT = """
INSERT INTO product_color VALUES(1, 'Blue');
INSERT INTO product_color VALUES(2, 'Black');
"""
SIZE_INSERT = """
INSERT INTO product_size VALUES(1, 'Small');
INSERT INTO product_size VALUES(2, 'Medium');
INSERT INTO product_size VALUES(3, 'Large');
"""
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
WHERE p.product_id = 200"""


async def example_1():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    version = connection.get_server_version()
    print(f'Подключено! Версия Postgres равна {version}')
    await connection.close()


async def example_2():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    statements = [CREATE_BRAND_TABLE, CREATE_PRODUCT_TABLE, CREATE_PRODUCT_COLOR_TABLE, CREATE_PRODUCT_SIZE_TABLE,
                  CREATE_SKU_TABLE, SIZE_INSERT, COLOR_INSERT]
    print('Создается база данных ...')
    for statement in statements:
        status = await connection.execute(statement)  # создание таблиц и вставка записей
        print(status)
    print('База данных создана!')
    await connection.close()


async def example_3():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")
    # fetch - выбор ВСЕХ марок из таблицы brand(все загружается в оперативную память), fetchrow - выбор одной записи:
    results: List[Record] = await connection.fetch("SELECT brand_id, brand_name FROM brand")
    # список из объектов Record, которые похожи на словари: можно обращаться к данным по имени столбца в индексе
    for brand in results:
        print(f'id: {brand["brand_id"]}, name: {brand["brand_name"]}')
    await connection.close()


def load_common_words() -> List[str]:
    with open('common_words.txt') as common_words:
        return common_words.readlines()


def generate_brand_names(words: List[str]) -> List[Tuple[Union[str, ]]]:
    return [(words[index],) for index in sample(range(100), 100)]


async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands_query = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands_query, brands)  # executemany выполняет параметризованную
    # SQL-команду, что позволит написать один запрос и передать ему список вставляемых записей в виде параметров,
    # а не создавать по одной команде INSERT для каждой марки


async def example_4():
    common_words = load_common_words()
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    await insert_brands(common_words, connection)


def gen_products(common_words: List[str],
                 brand_id_start: int,
                 brand_id_end: int,
                 products_to_create: int) -> List[Tuple[str, int]]:
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in sample(range(1000), 10)]
        brand_id = randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))
    return products


def gen_skus(product_id_start: int,
             product_id_end: int,
             skus_to_create: int) -> List[Tuple[int, int, int]]:
    skus = []
    for _ in range(skus_to_create):
        product_id = randint(product_id_start, product_id_end)
        size_id = randint(1, 3)
        color_id = randint(1, 2)
        skus.append((product_id, size_id, color_id))
    return skus


async def example_5():
    common_words = load_common_words()
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    product_tuples = gen_products(common_words, brand_id_start=1, brand_id_end=100, products_to_create=1000)
    # создание случайных product
    await connection.executemany("INSERT INTO product VALUES(DEFAULT, $1, $2)", product_tuples)  # заполнение product
    sku_tuples = gen_skus(product_id_start=1, product_id_end=1000, skus_to_create=100000)  # создание случайных sku
    await connection.executemany("INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)", sku_tuples)  # заполнение sku
    await connection.close()


async def query_product(pool):
    async with pool.acquire() as connection:  # acquire - контекстный менеджер для захвата соединения
        return await connection.fetchrow(product_query)  # fetchrow - выбор одной записи:


async def example_6():
    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5432,
                                   user='postgres',
                                   password='password',
                                   database='postgres',
                                   min_size=6,
                                   max_size=6) as pool:
        # create_pool - контекстный менеджер для создания пула подключений
        results = await asyncio.gather(query_product(pool),
                                       query_product(pool),
                                       query_product(pool),
                                       query_product(pool))
        # конкурентное выполнение 4 запросов для получения информации
        for result in results:
            print(result)


@async_timed()
async def query_products_synchronously(pool, queries):
    return [await query_product(pool) for _ in range(queries)]


@async_timed()
async def query_products_concurrently(pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


async def example_7():
    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5432,
                                   user='postgres',
                                   password='password',
                                   database='postgres',
                                   min_size=6,
                                   max_size=6) as pool:
        await query_products_synchronously(pool, 10000)
        await query_products_concurrently(pool, 10000)


async def example_8():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    async with connection.transaction():  # начало транзакции БД
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")
    query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)  # выбрать марки и убедиться, что транзакция была зафиксирована
    print(brands)
    await connection.close()


async def example_9():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
        await connection.execute(insert_brand)
        await connection.execute(insert_brand)  # из-за дубликата первичного ключа команда insert завершится неудачно
    except Exception as exp:
        logging.exception(f'Ошибка при выполнении транзакции: {exp}')
    finally:
        query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'big_%'"""
        brands = await connection.fetch(query)  # выбрать марки и убедиться, что ничего не вставлено
        print(f'Результат запроса: {brands}')
        await connection.close()


async def example_10():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    async with connection.transaction():  # исользуется для создания точки сохранения
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")
    try:
        async with connection.transaction():
            await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
    except Exception as exp:
        logging.warning('Ошибка при вставке цвета товара игнорируется', exc_info=exp)


async def example_11():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    transaction: Transaction = connection.transaction()
    await transaction.start()  # метод start необходим для старта транзакции
    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Ошибка, транзакция откатывается!')
        await transaction.rollback()  # если было исключение, то выполнить откат
    else:
        print('Ошибки нет, транзакция фиксируется!')
        await transaction.commit()  # если не было исключения, то выполнить фиксацию
    query = """SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)


async def positive_integers_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer


@async_timed()
async def example_12():
    async_generator = positive_integers_async(3)
    print(type(async_generator))
    async for number in async_generator:
        print(f'Получено число {number}')


async def example_13():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        async for product in connection.cursor(query):  # метод cursor возвращает асинхронный генератор, который
            # позволяет загружать в память данные порционно(по умолчанию параметр prefetch=50), таким образом происходит
            # потоковая обработка большого количества данных
            print(product)
    await connection.close()


async def example_14():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'
        cursor = await connection.cursor(query)  # создание курсора для запроса
        await cursor.forward(500)  # сдвинуть крусор вперед на 500 записей
        products = await cursor.fetch(100)  # получить следующие 100 записей
        for product in products:
            print(product)
    await connection.close()


async def take(generator, to_take: int):  # собственная асинхронная генераторная фун-я для получения первых пяти товаров
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count = item_count + 1
        yield item


async def example_15():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'
        product_generator = connection.cursor(query)
        async for product in take(product_generator, 5):
            print(product)
        print('Получены первые пять товаров!')
    await connection.close()


def main():
    asyncio.run(example_15())


if __name__ == '__main__':
    main()
