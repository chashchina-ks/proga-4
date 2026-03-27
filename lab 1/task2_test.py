import pytest
from task2 import my_genn, FibonacciLst

def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"

def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"

def test_fib_zero():
    gen = my_genn()
    assert gen.send(0) == [], "Запрос 0 элементов должен вернуть пустой список"

def test_fib_one():
    gen = my_genn()
    assert gen.send(1) == [0], "Запрос 1 элемента должен вернуть [0]"

def test_fib_two():
    gen = my_genn()
    assert gen.send(2) == [0, 1], "Запрос 2 элементов должен вернуть [0, 1]"

def test_fib_large():
    gen = my_genn()
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert gen.send(10) == expected, "Неверный список для 10 элементов"

def test_fib_independent_calls():
    gen = my_genn()
    list1 = gen.send(3)
    list2 = gen.send(3)
    assert list1 == list2 == [0, 1, 1], "Каждый вызов должен генерировать ряд с начала"

def test_fib_invalid_negative():
    gen = my_genn()
    try:
        gen.send(-5)
        assert False, "Должно быть выброшено исключение для отрицательного числа"
    except ValueError:
        pass

def test_fib_invalid_type():
    gen = my_genn()
    try:
        gen.send("abc")
        assert False, "Должно быть выброшено исключение для строки"
    except (ValueError, TypeError):
        pass

# Тесты для класса FibonacciLst
def test_fibonacci_lst_basic():
    fib_iter = FibonacciLst(max_count=5)
    assert list(fib_iter) == [0, 1, 1, 2, 3], "Базовый тест для FibonacciLst"

def test_fibonacci_lst_zero():
    fib_iter = FibonacciLst(max_count=0)
    assert list(fib_iter) == [], "Ноль элементов"

def test_fibonacci_lst_one():
    fib_iter = FibonacciLst(max_count=1)
    assert list(fib_iter) == [0], "Один элемент"

def test_fibonacci_lst_filter_example():
    pass # Ожидаемое поведение

if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v", "--tb=short"])
