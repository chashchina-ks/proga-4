"""
Модуль с тестами для сопрограммы Фибоначчи, использующей обычный итератор (__iter__ и __next__).
"""

import pytest
from normal_iter import my_genn

def test_fib_1():
    gen = my_genn()
    assert gen.send(3) == [0, 1, 1], "Тривиальный случай n = 3, список [0, 1, 1]"

def test_fib_2():
    gen = my_genn()
    assert gen.send(5) == [0, 1, 1, 2, 3], "Пять первых членов ряда"

# --- Тесты для крайних случаев ---

def test_fib_zero():
    """Проверка случая, когда запрошено 0 элементов"""
    gen = my_genn()
    assert gen.send(0) == [], "Запрос 0 элементов должен вернуть пустой список"

def test_fib_one():
    """Проверка случая, когда запрошен 1 элемент"""
    gen = my_genn()
    assert gen.send(1) == [0], "Запрос 1 элемента должен вернуть [0]"

def test_fib_two():
    """Проверка случая, когда запрошено 2 элемента"""
    gen = my_genn()
    assert gen.send(2) == [0, 1], "Запрос 2 элементов должен вернуть [0, 1]"

def test_fib_large():
    """Проверка большего количества элементов"""
    gen = my_genn()
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert gen.send(10) == expected, "Неверный список для 10 элементов"

def test_fib_independent_calls():
    """Проверка, что каждый вызов send начинает ряд заново"""
    gen = my_genn()
    list1 = gen.send(3)
    list2 = gen.send(3)
    assert list1 == list2 == [0, 1, 1], "Каждый вызов должен генерировать ряд с начала"

def test_fib_invalid_negative():
    """Проверка обработки отрицательного числа"""
    gen = my_genn()
    try:
        gen.send(-5)
        assert False, "Должно быть выброшено исключение для отрицательного числа"
    except ValueError:
        pass # Ожидаемое поведение

def test_fib_invalid_type():
    """Проверка обработки некорректного типа данных"""
    gen = my_genn()
    try:
        gen.send("abc")
        assert False, "Должно быть выброшено исключение для строки"
    except (ValueError, TypeError):
        pass # Ожидаемое поведение


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v", "--tb=short"])
