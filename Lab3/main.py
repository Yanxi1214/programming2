import unittest
from typing import Optional, Dict, Any


def gen_bin_tree(height: int = 4, root: int = 12) -> Optional[Dict[str, Any]]:
    """
    Рекурсивная функция генерации бинарного дерева
    
    Рекурсивно строит бинарное дерево на основе заданной высоты и значения корневого узла.
    Левый дочерний узел: root^3, правый дочерний узел: (root * 2) - 1.
    
    Args:
        height (int): Высота дерева, по умолчанию 4
        root (int): Значение корневого узла, по умолчанию 12
    
    Returns:
        Optional[Dict[str, Any]]: Словарь, представляющий бинарное дерево, или None если высота равна 0
        
    Examples:
        >>> tree = gen_bin_tree(3, 5)
        >>> tree = gen_bin_tree()  # использование параметров по умолчанию
    """
    # Базовый случай: если высота равна 0, возвращаем None
    if height == 0:
        return None
    
    # Рекурсивное построение бинарного дерева
    tree = {
        'root': root,
        'left': gen_bin_tree(height - 1, root ** 3),  # Левый дочерний узел: root^3
        'right': gen_bin_tree(height - 1, root * 2 - 1)  # Правый дочерний узел: (root * 2) - 1
    }
    
    return tree


class TestBinTree(unittest.TestCase):
    """Тестовый класс для функции генерации бинарного дерева"""
    
    def test_default_parameters(self):
        """Тестирование параметров по умолчанию"""
        tree = gen_bin_tree()
        self.assertIsNotNone(tree)
        self.assertEqual(tree['root'], 12)
    
    def test_zero_height(self):
        """Тестирование случая с высотой 0"""
        tree = gen_bin_tree(0, 5)
        self.assertIsNone(tree)
    
    def test_height_one(self):
        """Тестирование случая с высотой 1"""
        tree = gen_bin_tree(1, 10)
        expected = {
            'root': 10,
            'left': None,
            'right': None
        }
        self.assertEqual(tree, expected)
    
    def test_custom_parameters(self):
        """Тестирование пользовательских параметров"""
        tree = gen_bin_tree(2, 3)
        
        # Проверка корневого узла
        self.assertEqual(tree['root'], 3)
        
        # Проверка левого дочернего узла (3^3 = 27)
        self.assertEqual(tree['left']['root'], 27)
        
        # Проверка правого дочернего узла (3*2-1 = 5)
        self.assertEqual(tree['right']['root'], 5)
    
    def test_tree_structure_height_3(self):
        """Тестирование структуры дерева высотой 3"""
        tree = gen_bin_tree(3, 2)
        
        # Первый уровень
        self.assertEqual(tree['root'], 2)
        
        # Второй уровень - левое поддерево (2^3 = 8)
        self.assertEqual(tree['left']['root'], 8)
        # Второй уровень - правое поддерево (2*2-1 = 3)
        self.assertEqual(tree['right']['root'], 3)
        
        # Третий уровень - левое поддерево левого поддерева (8^3 = 512)
        self.assertEqual(tree['left']['left']['root'], 512)
        # Третий уровень - правое поддерево левого поддерева (8*2-1 = 15)
        self.assertEqual(tree['left']['right']['root'], 15)
        
        # Третий уровень - левое поддерево правого поддерева (3^3 = 27)
        self.assertEqual(tree['right']['left']['root'], 27)
        # Третий уровень - правое поддерево правого поддерева (3*2-1 = 5)
        self.assertEqual(tree['right']['right']['root'], 5)


def print_tree(tree: Dict[str, Any], level: int = 0) -> None:
    """
    Визуально отображает бинарное дерево в виде текста
    
    Args:
        tree (Dict[str, Any]): Бинарное дерево для печати
        level (int): Текущий уровень узла, используется для отступа
    """
    if tree is None:
        return
    
    indent = "  " * level
    print(f"{indent}root: {tree['root']}")
    
    if tree['left'] is not None:
        print(f"{indent}left:")
        print_tree(tree['left'], level + 1)
    
    if tree['right'] is not None:
        print(f"{indent}right:")
        print_tree(tree['right'], level + 1)


if __name__ == "__main__":
    # Запуск тестов
    print("Запуск тестов...")
    unittest.main(argv=[''], verbosity=2, exit=False)
    
    print("\n" + "="*50)
    print("Пример бинарного дерева (параметры по умолчанию):")
    print("="*50)
    
    # Генерация бинарного дерева с параметрами по умолчанию
    default_tree = gen_bin_tree()
    print("Словарное представление:")
    print(default_tree)
    
    print("\nДревовидная структура:")
    print_tree(default_tree)
    
    print("\n" + "="*50)
    print("Пример бинарного дерева (пользовательские параметры: height=3, root=2):")
    print("="*50)
    
    # Генерация бинарного дерева с пользовательскими параметрами
    custom_tree = gen_bin_tree(height=3, root=2)
    print("Словарное представление:")
    print(custom_tree)
    
    print("\nДревовидная структура:")
    print_tree(custom_tree)
