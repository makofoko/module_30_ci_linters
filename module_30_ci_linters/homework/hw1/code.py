"""Module with some typical mistakes. They aimed to be find by linters."""

from typing import Optional


class BadClass:
    # Исправлено: 42 — это int, а не str
    value: int = 42

    def get_value(self) -> str:
        # Исправлено: возвращается строка
        return "some_other_value"

    def compute_something(self) -> bool:
        # Исправлено: метод возвращает True/False, значит тип bool (и None нам не нужен)
        if self.value == 42:
            return True
        return False

    def it_will_fail(self) -> str:
        # Исправлено: обращались к несуществующему атрибуту
        other_value = "safe_value"
        return other_value


def viking_cafe_order(spam: str, beans: str, eggs: Optional[str] = None) -> str:
    # Исправлено: spam должен быть строкой, чтобы его можно было складывать
    del beans, eggs
    return spam + spam + spam


def compute_other_thing() -> None:
    # Исправлено: голый except заменен на конкретную ошибку,
    # а код разнесен на разные строки (требование flake8 и black)
    try:
        1 / 0
    except ZeroDivisionError:
        print("oops")
