"""
Модульные тесты для функций генерации бинарных деревьев.

Тесты охватывают различные сценарии, включая параметры по умолчанию, 
пользовательские параметры, граничные случаи и различные структуры деревьев.
"""

import unittest
from main import gen_bin_tree, tree_to_list, get_tree_height, gen_bin_tree_class, TreeNode


class TestBinaryTree(unittest.TestCase):
    """Тестовые случаи для генерации бинарных деревьев."""
    
    def test_default_parameters_variant_12(self):
        """Тест генерации дерева с параметрами по умолчанию (вариант 12)."""
        tree = gen_bin_tree()
        
        # Проверка значения корня
        self.assertEqual(tree['value'], 12)
        
        # Проверка высоты дерева
        self.assertEqual(get_tree_height(tree), 4)
        
        # Проверка левого и правого потомков корня
        self.assertEqual(tree['left']['value'], 1728)  # 12 ** 3
        self.assertEqual(tree['right']['value'], 23)   # (12 * 2) - 1
        
    def test_custom_variant_1(self):
        """Тест с параметрами варианта 1."""
        tree = gen_bin_tree(
            height=5,
            root=1,
            left_leaf=lambda x: x * 2,
            right_leaf=lambda x: x + 3
        )
        
        self.assertEqual(tree['value'], 1)
        self.assertEqual(get_tree_height(tree), 5)
        self.assertEqual(tree['left']['value'], 2)  # 1 * 2
        self.assertEqual(tree['right']['value'], 4)  # 1 + 3
        
    def test_custom_variant_2(self):
        """Тест с параметрами варианта 2."""
        tree = gen_bin_tree(
            height=3,
            root=2,
            left_leaf=lambda x: x * 3,
            right_leaf=lambda x: x + 4
        )
        
        self.assertEqual(tree['value'], 2)
        self.assertEqual(get_tree_height(tree), 3)
        self.assertEqual(tree['left']['value'], 6)  # 2 * 3
        self.assertEqual(tree['right']['value'], 6)  # 2 + 4
        
    def test_zero_height(self):
        """Тест с высотой 0 (пустое дерево)."""
        tree = gen_bin_tree(height=0)
        self.assertIsNone(tree)
        
    def test_height_one(self):
        """Тест с высотой 1 (только корень)."""
        tree = gen_bin_tree(height=1, root=10)
        self.assertEqual(tree['value'], 10)
        self.assertIsNone(tree['left'])
        self.assertIsNone(tree['right'])
        
    def test_negative_height(self):
        """Тест с отрицательной высотой (должна вызывать ошибку)."""
        with self.assertRaises(ValueError):
            gen_bin_tree(height=-1)
            
    def test_invalid_left_leaf(self):
        """Тест с неверной функцией left_leaf."""
        with self.assertRaises(TypeError):
            gen_bin_tree(left_leaf="not_a_function")
            
    def test_invalid_right_leaf(self):
        """Тест с неверной функцией right_leaf."""
        with self.assertRaises(TypeError):
            gen_bin_tree(right_leaf=123)
            
    def test_tree_to_list(self):
        """Тест преобразования дерева в список."""
        tree = gen_bin_tree(height=3, root=1)
        result = tree_to_list(tree)
        self.assertEqual(len(result), 7)  # 1 + 2 + 4 узлов для высоты 3
        
    def test_complex_leaf_functions(self):
        """Тест со сложными функциями генерации листьев."""
        tree = gen_bin_tree(
            height=3,
            root=5,
            left_leaf=lambda x: x ** 2,  # x^2
            right_leaf=lambda x: x - 2
        )
        
        self.assertEqual(tree['value'], 5)
        self.assertEqual(tree['left']['value'], 25)  # 5^2
        self.assertEqual(tree['right']['value'], 3)  # 5-2
        self.assertEqual(tree['left']['left']['value'], 625)  # 25^2
        
    def test_tree_node_class(self):
        """Тест генерации дерева с классом TreeNode."""
        tree = gen_bin_tree_class(height=2, root=10)
        
        self.assertIsInstance(tree, TreeNode)
        self.assertEqual(tree.value, 10)
        self.assertEqual(tree.left.value, 1000)  # 10 ** 3
        self.assertEqual(tree.right.value, 19)   # (10 * 2) - 1
        
    def test_tree_node_to_dict(self):
        """Тест преобразования TreeNode в словарь."""
        tree = gen_bin_tree_class(height=2, root=10)
        tree_dict = tree.to_dict()
        
        self.assertEqual(tree_dict['value'], 10)
        self.assertEqual(tree_dict['left']['value'], 1000)
        self.assertEqual(tree_dict['right']['value'], 19)
        
    def test_different_data_types(self):
        """Тест с различными типами данных в качестве значений узлов."""
        # Тест со строковым корнем
        tree = gen_bin_tree(height=2, root="A")
        self.assertEqual(tree['value'], "A")
        
        # Тест с вещественным корнем
        tree = gen_bin_tree(height=2, root=1.5)
        self.assertEqual(tree['value'], 1.5)
        
    def test_edge_case_height_large(self):
        """Тест с относительно большой высотой."""
        tree = gen_bin_tree(height=10)
        self.assertEqual(get_tree_height(tree), 10)
        
    def test_level_order_correctness(self):
        """Тест правильности построения дерева в порядке уровней."""
        tree = gen_bin_tree(height=3, root=2)
        
        # Уровень корня
        self.assertEqual(tree['value'], 2)
        
        # Первый уровень
        self.assertEqual(tree['left']['value'], 8)   # 2 ** 3
        self.assertEqual(tree['right']['value'], 3)  # (2 * 2) - 1
        
        # Второй уровень
        self.assertEqual(tree['left']['left']['value'], 512)   # 8 ** 3
        self.assertEqual(tree['left']['right']['value'], 15)   # (8 * 2) - 1
        self.assertEqual(tree['right']['left']['value'], 27)   # 3 ** 3
        self.assertEqual(tree['right']['right']['value'], 5)   # (3 * 2) - 1
        
    def test_variant_12_specific(self):
        """Тест специфических вычислений для варианта 12."""
        tree = gen_bin_tree()  # Вариант 12 по умолчанию
        
        # Уровень корня
        self.assertEqual(tree['value'], 12)
        
        # Первый уровень
        self.assertEqual(tree['left']['value'], 1728)  # 12^3
        self.assertEqual(tree['right']['value'], 23)   # (12*2)-1
        
        # Второй уровень - левое поддерево
        self.assertEqual(tree['left']['left']['value'], 1728**3)
        self.assertEqual(tree['left']['right']['value'], (1728*2)-1)
        
        # Второй уровень - правое поддерево  
        self.assertEqual(tree['right']['left']['value'], 23**3)
        self.assertEqual(tree['right']['right']['value'], (23*2)-1)


if __name__ == '__main__':
    # Для совместимости с Google Colab
    unittest.main(argv=[''], verbosity=2, exit=False)
