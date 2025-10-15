import unittest
from main import two_sum


class TestTwoSum(unittest.TestCase):
    """Тестирует функцию two_sum"""
    
    def test_example1(self):
        """Тест примера 1: nums = [2,7,11,15], target = 9"""
        nums = [2, 7, 11, 15]
        target = 9
        expected = [0, 1]
        result = two_sum(nums, target)
        self.assertEqual(result, expected)
    
    def test_example2(self):
        """Тест примера 2: nums = [3,2,4], target = 6"""
        nums = [3, 2, 4]
        target = 6
        expected = [1, 2]
        result = two_sum(nums, target)
        self.assertEqual(result, expected)
    
    def test_example3(self):
        """Тест примера 3: nums = [3,3], target = 6"""
        nums = [3, 3]
        target = 6
        expected = [0, 1]
        result = two_sum(nums, target)
        self.assertEqual(result, expected)
    
    def test_no_solution(self):
        """Тест случая без решения"""
        nums = [1, 2, 3]
        target = 7
        expected = []
        result = two_sum(nums, target)
        self.assertEqual(result, expected)
    
    def test_negative_numbers(self):
        """Тест с отрицательными числами"""
        nums = [-1, -2, -3, -4, -5]
        target = -8
        expected = [2, 4]
        result = two_sum(nums, target)
        self.assertEqual(result, expected)
    
    def test_duplicate_numbers(self):
        """Тест с повторяющимися числами, но разными индексами"""
        nums = [3, 2, 3]
        target = 6
        expected = [0, 2]
        result = two_sum(nums, target)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    # Запуск тестов
    unittest.main(verbosity=2)
