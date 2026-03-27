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

def my_genn():
    """Сопрограмма: принимает число n через send(), возвращает список из первых n чисел Фибоначчи"""
    while True:
        # Получаем количество элементов через send()
        number_of_fib_elem = yield

        # Простая валидация входных данных
        if not isinstance(number_of_fib_elem, int) or number_of_fib_elem < 0:
            raise ValueError("Ожидается неотрицательное целое число")

        # Создаем новый генератор для каждого запроса, чтобы начать ряд с начала
        local_fib = fib_elem_gen()

        # Генерируем список, используя встроенную функцию next() для генератора
        result = [next(local_fib) for _ in range(number_of_fib_elem)]

        yield result

def fib_coroutine(g):
    """Декоратор для автоматического запуска корутины до первого yield"""
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)  # Запускаем генератор
        return gen
    return inner

# Применяем декоратор
my_genn = fib_coroutine(my_genn)

# Пример использования (можно закомментировать при импорте в тестах)
if __name__ == "__main__":
    gen = my_genn()
    print(gen.send(3))   # Ожидается: [0, 1, 1]
    print(gen.send(5))   # Ожидается: [0, 1, 1, 2, 3]
    print(gen.send(8))   # Ожидается: [0, 1, 1, 2, 3, 5, 8, 13]
