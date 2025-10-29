import unittest
from main import (
    fact_recursive,
    fact_iterative,
    fact_recursive_memo,
    fact_iterative_memo,
    fact_iter_memo_cache  # Импорт кэша для итеративной мемоизации (для сброса)
)


class TestFactorialFunctions(unittest.TestCase):
    """Тестирование корректности всех функций вычисления факториала"""

    # Тестовые случаи: (входное n, ожидаемый результат) — покрываем 0, 1, малые и большие значения
    VALID_TEST_CASES = [
        (0, 1),
        (1, 1),
        (2, 2),
        (5, 120),
        (10, 3628800),
        (15, 1307674368000),
        (20, 2432902008176640000)
    ]

    # Тестовые случаи с отрицательными числами (ожидаем выброс ValueError)
    INVALID_TEST_CASES = [-1, -5, -10, -20]

    def setUp(self):
        """Сброс кэша итеративной мемоизации перед каждым тестом (гарантируем независимость тестов)"""
        fact_iter_memo_cache.clear()
        fact_iter_memo_cache.update({0: 1, 1: 1})

    def test_valid_inputs(self):
        """Тестирование корректности результатов при допустимых входных данных (неотрицательные целые)"""
        # Список всех тестируемых функций
        functions = [
            fact_recursive,
            fact_iterative,
            fact_recursive_memo,
            fact_iterative_memo
        ]

        # Проверка каждой функции для каждого тестового случая
        for func in functions:
            with self.subTest(func_name=func.__name__):  # Маркируем подтесты для удобства поиска ошибок
                for n, expected in self.VALID_TEST_CASES:
                    result = func(n)
                    self.assertEqual(
                        result, expected,
                        msg=f"{func.__name__}({n}) ошибка: ожидается {expected}, получено {result}"
                    )

    def test_invalid_inputs(self):
        """Тестирование выброса исключения ValueError при недопустимых входных данных (отрицательные числа)"""
        functions = [
            fact_recursive,
            fact_iterative,
            fact_recursive_memo,
            fact_iterative_memo
        ]

        for func in functions:
            with self.subTest(func_name=func.__name__):
                for n in self.INVALID_TEST_CASES:
                    with self.assertRaises(
                        ValueError,
                        msg=f"{func.__name__}({n}) не выбросило исключение ValueError"
                    ):
                        func(n)


if __name__ == "__main__":
    # Запуск всех тестовых случаев
    unittest.main()
