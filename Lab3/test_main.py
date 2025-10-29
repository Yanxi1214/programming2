import unittest
import json
from binary_tree import gen_bin_tree


class TestBinTree(unittest.TestCase):
    """Тестовый класс для функции генерации бинарного дерева"""
    
    def test_default_parameters(self):
        """Тестирование параметров по умолчанию"""
        tree = gen_bin_tree()
        self.assertIsNotNone(tree)
        self.assertEqual(tree['value'], 12)
        
        # Проверка структуры дерева
        expected_structure = {
            'value': 12,
            'left': {
                'value': 1728,
                'left': {
                    'value': 5159780352,
                    'left': None,
                    'right': None
                },
                'right': {
                    'value': 3455,
                    'left': None,
                    'right': None
                }
            },
            'right': {
                'value': 23,
                'left': {
                    'value': 12167,
                    'left': None,
                    'right': None
                },
                'right': {
                    'value': 45,
                    'left': None,
                    'right': None
                }
            }
        }
        self.assertEqual(tree, expected_structure)
    
    def test_zero_height(self):
        """Тестирование случая с высотой 0"""
        tree = gen_bin_tree(0, 5)
        self.assertIsNone(tree)
    
    def test_negative_height(self):
        """Тестирование отрицательной высоты"""
        tree = gen_bin_tree(-1, 5)
        self.assertIsNone(tree)
    
    def test_height_one(self):
        """Тестирование случая с высотой 1"""
        tree = gen_bin_tree(1, 10)
        expected = {
            'value': 10,
            'left': None,
            'right': None
        }
        self.assertEqual(tree, expected)
    
    def test_custom_functions(self):
        """Тестирование пользовательских функций для потомков"""
        tree = gen_bin_tree(
            height=2, 
            root=3, 
            left_leaf=lambda x: x + 2,
            right_leaf=lambda x: x * 3
        )
        
        expected = {
            'value': 3,
            'left': {
                'value': 5,
                'left': None,
                'right': None
            },
            'right': {
                'value': 9,
                'left': None,
                'right': None
            }
        }
        self.assertEqual(tree, expected)
    
    def test_variant_parameters(self):
        """Тестирование параметров из варианта задания"""
        # Вариант: root = 1, height = 5, left_leaf = root * 2, right_leaf = root + 3
        tree = gen_bin_tree(
            height=2,
            root=1,
            left_leaf=lambda x: x * 2,
            right_leaf=lambda x: x + 3
        )
        
        expected = {
            'value': 1,
            'left': {
                'value': 2,
                'left': None,
                'right': None
            },
            'right': {
                'value': 4,
                'left': None,
                'right': None
            }
        }
        self.assertEqual(tree, expected)
    
    def test_complex_tree_structure(self):
        """Тестирование сложной структуры дерева"""
        tree = gen_bin_tree(
            height=3,
            root=2,
            left_leaf=lambda x: x * 2,
            right_leaf=lambda x: x + 1
        )
        
        # Проверка полной структуры дерева
        self.assertEqual(tree['value'], 2)
        self.assertEqual(tree['left']['value'], 4)
        self.assertEqual(tree['right']['value'], 3)
        self.assertEqual(tree['left']['left']['value'], 8)
        self.assertEqual(tree['left']['right']['value'], 5)
        self.assertEqual(tree['right']['left']['value'], 6)
        self.assertEqual(tree['right']['right']['value'], 4)


if __name__ == "__main__":
    # Запуск тестов
    unittest.main(argv=[''], verbosity=2, exit=False)
