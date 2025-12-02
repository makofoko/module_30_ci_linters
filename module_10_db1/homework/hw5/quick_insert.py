from typing import Union, List

Number = Union[int, float, complex]

def find_insert_position(array: List[Number], number: Number) -> int:
    left, right = 0, len(array)
    while left < right:
        mid = (left + right) // 2
        if array[mid] < number:
            left = mid + 1
        else:
            right = mid
    return left

if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    print("Позиция для вставки:", insert_position)
    assert insert_position == 5

    A.insert(insert_position, x)
    print("Массив после вставки:", A)
    assert A == sorted(A)
