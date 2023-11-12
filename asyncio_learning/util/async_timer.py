import functools
import time
from typing import Callable, Any


def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        # декоратор functools.wraps необходим для того, чтобы копировалось имя, строка документации и сигнатура функции
        # в нашу внутреннюю функцию
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Выполняется функция {func} с аргументами {args} {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'Функция {func} завершилась за {total:.3f} с')
        return wrapped
    return wrapper
