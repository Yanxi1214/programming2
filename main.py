"""
Модуль для нерекурсивного генерации бинарных деревьев.

Этот модуль предоставляет функциональность для создания бинарных деревьев 
с заданной высотой и правилами генерации узлов с использованием итеративных подходов.
"""

from collections import deque
from typing import Any, Callable, Optional, Dict


def gen_bin_tree(
    height: Optional[int] = None,
    root: Optional[Any] = None,
    left_leaf: Optional[Callable[[Any], Any]] = None,
    right_leaf: Optional[Callable[[Any], Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Генерирует бинарное дерево нерекурсивным способом с заданными параметрами.
    
    Если параметры не предоставлены, используются значения по умолчанию из варианта 12:
    - root: 12
    - height: 4  
    - left_leaf: lambda x: x ** 3
    - right_leaf: lambda x: (x * 2) - 1
    
    Аргументы:
        height: Высота дерева (количество уровней)
        root: Значение корневого узла
        left_leaf: Функция для вычисления значения левого потомка из значения родителя
        right_leaf: Функция для вычисления значения правого потомка из значения родителя
        
    Возвращает:
        Словарь, представляющий структуру бинарного дерева с ключами:
        'value', 'left', 'right'. Возвращает None если высота равна 0.
        
    Вызывает:
        ValueError: Если высота отрицательная
        TypeError: Если left_leaf или right_leaf не являются вызываемыми объектами
    """
    # Установка значений по умолчанию если не предоставлены (вариант 12)
    if height is None:
        height = 4
    if root is None:
        root = 12
    if left_leaf is None:
        left_leaf = lambda x: x ** 3
    if right_leaf is None:
        right_leaf = lambda x: (x * 2) - 1
    
    # Проверка входных данных
    if height < 0:
        raise ValueError("Высота не может быть отрицательной")
    if not callable(left_leaf):
        raise TypeError("left_leaf должен быть вызываемым объектом")
    if not callable(right_leaf):
        raise TypeError("right_leaf должен быть вызываемым объектом")
    
    # Возврат None для пустого дерева
    if height == 0:
        return None
    
    # Создание корневого узла
    tree = {'value': root, 'left': None, 'right': None}
    
    # Использование очереди для обхода в ширину (нерекурсивный подход)
    queue = deque()
    queue.append((tree, 1))  # (узел, текущая_глубина)
    
    while queue:
        current_node, current_depth = queue.popleft()
        
        # Остановка построения если достигнута желаемая высота
        if current_depth >= height:
            continue
            
        # Создание левого потомка
        left_value = left_leaf(current_node['value'])
        current_node['left'] = {'value': left_value, 'left': None, 'right': None}
        queue.append((current_node['left'], current_depth + 1))
        
        # Создание правого потомка  
        right_value = right_leaf(current_node['value'])
        current_node['right'] = {'value': right_value, 'left': None, 'right': None}
        queue.append((current_node['right'], current_depth + 1))
    
    return tree


def tree_to_list(tree: Optional[Dict[str, Any]]) -> list:
    """
    Преобразует словарь бинарного дерева в представление в виде списка (в порядке уровней).
    
    Полезно для тестирования и визуализации.
    
    Аргументы:
        tree: Словарь бинарного дерева
        
    Возвращает:
        Список значений узлов в порядке уровней, None для отсутствующих узлов
    """
    if not tree:
        return []
    
    result = []
    queue = deque([tree])
    
    while queue:
        current = queue.popleft()
        if current:
            result.append(current['value'])
            queue.append(current.get('left'))
            queue.append(current.get('right'))
        else:
            result.append(None)
    
    # Удаление конечных значений None
    while result and result[-1] is None:
        result.pop()
        
    return result


def get_tree_height(tree: Optional[Dict[str, Any]]) -> int:
    """
    Вычисляет высоту бинарного дерева.
    
    Аргументы:
        tree: Словарь бинарного дерева
        
    Возвращает:
        Высота дерева (0 для пустого дерева)
    """
    if not tree:
        return 0
    
    queue = deque([(tree, 1)])
    max_depth = 0
    
    while queue:
        current_node, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        
        if current_node.get('left'):
            queue.append((current_node['left'], depth + 1))
        if current_node.get('right'):
            queue.append((current_node['right'], depth + 1))
            
    return max_depth


# Альтернативная реализация с использованием класса Node
class TreeNode:
    """Класс узла для бинарного дерева с использованием пользовательского класса вместо словаря."""
    
    def __init__(self, value: Any):
        self.value = value
        self.left = None
        self.right = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует TreeNode в представление в виде словаря."""
        result = {'value': self.value, 'left': None, 'right': None}
        if self.left:
            result['left'] = self.left.to_dict()
        if self.right:
            result['right'] = self.right.to_dict()
        return result


def gen_bin_tree_class(
    height: Optional[int] = None,
    root: Optional[Any] = None, 
    left_leaf: Optional[Callable[[Any], Any]] = None,
    right_leaf: Optional[Callable[[Any], Any]] = None
) -> Optional[TreeNode]:
    """
    Генерирует бинарное дерево с использованием класса TreeNode вместо словаря.
    
    Использует те же параметры и логику, что и gen_bin_tree, но возвращает
    экземпляры TreeNode вместо словарей.
    """
    if height is None:
        height = 4
    if root is None:
        root = 12
    if left_leaf is None:
        left_leaf = lambda x: x ** 3
    if right_leaf is None:
        right_leaf = lambda x: (x * 2) - 1
    
    if height == 0:
        return None
    
    root_node = TreeNode(root)
    queue = deque()
    queue.append((root_node, 1))
    
    while queue:
        current_node, current_depth = queue.popleft()
        
        if current_depth >= height:
            continue
            
        left_value = left_leaf(current_node.value)
        current_node.left = TreeNode(left_value)
        queue.append((current_node.left, current_depth + 1))
        
        right_value = right_leaf(current_node.value)
        current_node.right = TreeNode(right_value)
        queue.append((current_node.right, current_depth + 1))
    
    return root_node
