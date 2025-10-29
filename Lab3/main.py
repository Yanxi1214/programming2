import json
from typing import Optional, Dict, Any, Callable


def gen_bin_tree(
    height: int = 4, 
    root: int = 12, 
    left_leaf: Optional[Callable[[int], int]] = None,
    right_leaf: Optional[Callable[[int], int]] = None
) -> Optional[Dict[str, Any]]:
    """
    Рекурсивная функция генерации бинарного дерева
    
    Рекурсивно строит бинарное дерево на основе заданной высоты, значения корневого узла
    и функций для вычисления левого и правого потомков.
    
    Args:
        height (int): Высота дерева. Если height <= 0, возвращает None.
        root (int): Значение корневого узла.
        left_leaf (Callable): Функция для вычисления значения левого потомка. 
                             По умолчанию: lambda x: x ** 3
        right_leaf (Callable): Функция для вычисления значения правого потомка.
                              По умолчанию: lambda x: (x * 2) - 1
    
    Returns:
        Optional[Dict[str, Any]]: Словарь, представляющий бинарное дерево, 
                                 или None если высота <= 0
        
    Examples:
        >>> tree = gen_bin_tree(3, 5)
        >>> tree = gen_bin_tree()  # использование параметров по умолчанию
        >>> tree = gen_bin_tree(3, 2, lambda x: x*2, lambda x: x+1)
    """
    # Обработка отрицательной высоты
    if height <= 0:
        return None
    
    # Установка функций по умолчанию
    if left_leaf is None:
        left_leaf = lambda x: x ** 3
    if right_leaf is None:
        right_leaf = lambda x: (x * 2) - 1
    
    # Вычисление значений потомков
    left_value = left_leaf(root)
    right_value = right_leaf(root)
    
    # Рекурсивное построение бинарного дерева
    tree = {
        'value': root,
        'left': gen_bin_tree(height - 1, left_value, left_leaf, right_leaf),
        'right': gen_bin_tree(height - 1, right_value, left_leaf, right_leaf)
    }
    
    return tree


if __name__ == "__main__":
    # Демонстрация работы функции с параметрами по умолчанию
    default_tree = gen_bin_tree()
    print("Бинарное дерево с параметрами по умолчанию:")
    print(json.dumps(default_tree, indent=2))
    
    print("\n" + "="*50)
    
    # Демонстрация работы с пользовательскими параметрами
    custom_tree = gen_bin_tree(
        height=3, 
        root=2, 
        left_leaf=lambda x: x * 2,
        right_leaf=lambda x: x + 3
    )
    print("Бинарное дерево с пользовательскими параметрами:")
    print(json.dumps(custom_tree, indent=2))

