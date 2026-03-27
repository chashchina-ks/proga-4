"""
Модуль с тестами для сопрограммы Фибоначчи, использующей упрощенный итератор (__getitem__).
"""

import pytest
from simple_iter import my_genn

def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"

def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"

def test_fib_zero():
    gen = my_genn()
    assert gen.send(0) == [], "Ноль элементов — пустой список"

def test_fib_one():
    gen = my_genn()
    assert gen.send(1) == [0], "Один элемент — [0]"

def test_fib_two():
    gen = my_genn()
    assert gen.send(2) == [0, 1], "Два элемента — [0, 1]"

def test_fib_large():
    gen = my_genn()
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert gen.send(10) == expected, "Десять первых членов ряда"

def test_fib_invalid_input():
    gen = my_genn()
    try:
        gen.send(-1)
        assert False, "Должно быть выброшено исключение для отрицательного числа"
    except ValueError:
        pass  # ожидаемое поведение

    try:
        gen.send("abc")
        assert False, "Должно быть выброшено исключение для строки"
    except (ValueError, TypeError):
        pass  # допускаем либо ValueError, либо TypeError


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v", "--tb=short"])
