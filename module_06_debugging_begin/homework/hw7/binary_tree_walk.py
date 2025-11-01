import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> Optional[BinaryTreeNode]:
    """
    Восстанавливает дерево из файла лога, созданного функцией walk (BFS).
    """

    nodes_map = {}
    root_val = None


    info_pattern = re.compile(r"INFO:Visiting <BinaryTreeNode\[(\d+)\]>")

    debug_pattern = re.compile(
        r"DEBUG:<BinaryTreeNode\[(\d+)\]> (left|right) is not empty\. Adding <BinaryTreeNode\[(\d+)\]> to the queue"
    )

    try:
        with open(path_to_log_file, 'r') as f:
            for line in f:
                stripped_line = line.strip()

                debug_match = debug_pattern.match(stripped_line)
                if debug_match:
                    parent_val = int(debug_match.group(1))
                    direction = debug_match.group(2)
                    child_val = int(debug_match.group(3))

                    if parent_val not in nodes_map:
                        nodes_map[parent_val] = BinaryTreeNode(val=parent_val)
                    parent_node = nodes_map[parent_val]

                    if child_val not in nodes_map:
                        nodes_map[child_val] = BinaryTreeNode(val=child_val)
                    child_node = nodes_map[child_val]

                    if direction == 'left':
                        parent_node.left = child_node
                    else:
                        parent_node.right = child_node

                elif root_val is None:
                    info_match = info_pattern.match(stripped_line)
                    if info_match:
                        root_val = int(info_match.group(1))
                        if root_val not in nodes_map:
                            nodes_map[root_val] = BinaryTreeNode(val=root_val)

    except FileNotFoundError:
        print(f"Ошибка: Файл логов не найден по пути {path_to_log_file}")
        return None
    except Exception as e:
        print(f"Ошибка при парсинге файла: {e}")
        return None

    if root_val is not None:
        return nodes_map.get(root_val)

    return None

if __name__ == "__main__":
    LOG_FILE = "walk_log_4.txt"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename=LOG_FILE,
        filemode='w'
    )

    print(f"Генерация дерева и запись логов в {LOG_FILE}...")
    root = get_tree(7)

    if root:
        print(f"Оригинальный корень: {root!r}")
        walk(root)
        print("Запись логов завершена.")
    else:
        print("Дерево не было создано.")
        exit()

    print("\nВосстановление дерева из лога...")
    restored_root = restore_tree(LOG_FILE)

    if restored_root:
        print(f"Восстановленный корень: {restored_root!r}")

        if root.val == restored_root.val:
            print("УСПЕХ: Корень восстановлен правильно.")
        else:
            print("ОШИБКА: Значения корней не совпадают.")
    else:
        print("ОШИБКА: Восстановление дерева не удалось.")