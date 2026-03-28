import functools

class FibIterator:
    """Класс-итератор для генерации чисел Фибоначчи"""
    def __init__(self):
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        current = self.a
        self.a, self.b = self.b, self.a + self.b
        return current

def my_genn():
    """Сопрограмма: принимает число n через send(), возвращает список из первых n чисел Фибоначчи"""
    while True:
        # Получаем количество элементов через send()
        number_of_fib_elem = yield

        # Проверка на корректность ввода (опционально, но полезно для тестов)
        if not isinstance(number_of_fib_elem, int) or number_of_fib_elem < 0:
            raise ValueError("Ожидается неотрицательное целое число")

        # Создаем новый экземпляр итератора для каждого запроса, чтобы начать с начала ряда
        fib_iter = FibIterator()

        # Генерируем список, используя наш итератор
        result = []
        for _ in range(number_of_fib_elem):
            result.append(next(fib_iter))

        yield result

def fib_coroutine(g):
    """Декоратор для автоматического запуска корутины до первого yield"""
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)  # Запускаем генератор (эквивалент gen.send(None))
        return gen
    return inner

# Применяем декоратор
my_genn = fib_coroutine(my_genn)
