from flask import Flask

app = Flask(__name__)


class BadClass:
    def __init__(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return self.value


def create_bad_class(value: int) -> BadClass:
    return BadClass(value)