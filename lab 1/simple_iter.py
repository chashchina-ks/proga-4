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
    fib_gen = fib_elem_gen()  

    while True:
        number_of_fib_elem = yield
        if not isinstance(number_of_fib_elem, int) or number_of_fib_elem < 0:
            raise ValueError("Ожидается неотрицательное целое число")

        # Создаем новый генератор для каждого запроса, чтобы начать с начала
        local_fib = fib_elem_gen()
        result = []
        for _ in range(number_of_fib_elem):
            result.append(next(local_fib))
        yield result

def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)  # запускаем до первого yield
        return gen
    return inner

my_genn = fib_coroutine(my_genn)

# Пример использования (можно закомментировать при импорте)
if __name__ == "__main__":
    gen = my_genn()
    print(gen.send(3))   # [0, 1, 1]
    print(gen.send(5))   # [0, 1, 1, 2, 3]
    print(gen.send(8))   # [0, 1, 1, 2, 3, 5, 8, 13]
