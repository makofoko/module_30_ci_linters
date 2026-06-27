"""Module with some typical mistakes. They aimed to be find by linters."""
from typing import Optional

class BadClass:
    value: int = 42

    def get_value(self) -> str:
        return "some_other_value"

    def compute_something(self) -> bool:
        if self.value == 42:
            return True
        return False

    def it_will_fail(self) -> str:
        other_value = "safe_value"
        return other_value

def viking_cafe_order(spam: str, beans: str, eggs: Optional[str] = None) -> str:
    del beans, eggs
    return spam + spam + spam

def compute_other_thing() -> None:
    try:
        1 / 0
    except ZeroDivisionError:
        print("oops")