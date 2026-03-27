import functools

def fib_elem_gen():
    """Генератор, возвращающий элементы ряда Фибоначчи"""
    a = 0
    b = 1
    while True:
        yield a
        res = a + b
        a = b
        b = res

class FibonacciLst:
    """Класс-итератор, генерирующий числа Фибоначчи"""
    def __init__(self, max_count=None):
        """
        max_count: максимальное количество элементов для генерации
        """
        self.max_count = max_count
        self.count = 0
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.max_count is not None and self.count >= self.max_count:
            raise StopIteration
        current = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return current

def my_genn():
    """Сопрограмма: принимает число n через send(), возвращает список из первых n чисел Фибоначчи"""
    while True:
        number_of_fib_elem = yield

        if not isinstance(number_of_fib_elem, int) or number_of_fib_elem < 0:
            raise ValueError("Ожидается неотрицательное целое число")

        # Используем наш класс-итератор для генерации ряда
        fib_iter = FibonacciLst(max_count=number_of_fib_elem)
        result = list(fib_iter)

        yield result

def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)  # Запускаем генератор
        return gen
    return inner

my_genn = fib_coroutine(my_genn)

# Пример использования
if __name__ == "__main__":
    gen = my_genn()
    print(gen.send(3))   # [0, 1, 1]
    print(gen.send(5))   # [0, 1, 1, 2, 3]
    print(gen.send(8))   # [0, 1, 1, 2, 3, 5, 8, 13]

    # Пример использования FibonacciLst напрямую
    fib_lst = FibonacciLst(max_count=10)
    print(list(fib_lst))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
