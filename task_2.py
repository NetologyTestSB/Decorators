import os
import functools
from datetime import datetime
import time

def write_info_to_log_file(path, info):
    with open(path, 'a', encoding='utf-8') as flog:
        flog.write(info)

def logger(path):
    call_count = 0

    def __logger(old_function):

        @functools.wraps(old_function)
        def new_function(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            func_call_time = datetime.now()
            start = time.perf_counter()
            result = old_function(*args, **kwargs)
            stop = time.perf_counter()
            info_str = datetime.strftime(func_call_time, '%d.%m.%Y %H:%M:%S')
            arg_str = (str(args) if args else '') + ' ' + (str(kwargs) if kwargs else '')
            if arg_str == ' ':
                arg_str = 'без аргументов'
            info_str += f'\n\tвызов функции: {old_function.__name__}\n' \
                        f'\tаргументы: {arg_str} \n' \
                        f'\tрезультат: {result}\n' \
                        f'\tвремя выполнения: {(stop - start):1.7f} сек\n' \
                        f'\tпорядковый номер вызова: {call_count}\n'
            write_info_to_log_file(path, info_str)
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
