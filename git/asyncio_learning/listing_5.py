import asyncpg
import asyncio


async def example_1():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='postgres',
                                       password='password')
    version = connection.get_server_version()
    print(f'Подключено! Версия Postgres равна {version}')
    await connection.close()


def main():
    asyncio.run(example_1())


if __name__ == '__main__':
    main()
