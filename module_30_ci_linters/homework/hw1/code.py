from typing import Optional

class BadClass:
    def __init__(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return self.value

# Исправленная функция: возвращает объект, а не строку
def create_bad_class(value: int) -> BadClass:
    return BadClass(value)

# Исправленная функция: явно возвращаем значение
def check_logic(val: Optional[int]) -> int:
    if val is None:
        return 0
    return val + 10  # Теперь mypy знает, что val не None