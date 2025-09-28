from flask import Flask
from markupsafe import escape

app = Flask(__name__)


def is_number(value: str) -> bool:
    """
    Проверяет, можно ли строку преобразовать в число (int или float).
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


@app.route("/max_number/<path:numbers>")
def max_number(numbers: str) -> str:
    """
    Endpoint, который принимает список чисел через слеш
    и возвращает максимальное из них.
    """
    parts = numbers.split("/")
    valid_numbers = []

    for part in parts:
        if is_number(part):
            valid_numbers.append(float(part))
        else:
            return f"Ошибка: '{escape(part)}' не является числом."

    if not valid_numbers:
        return "Ошибка: не передано ни одного числа."

    max_num = max(valid_numbers)

    if max_num.is_integer():
        max_num = int(max_num)

    return f"Максимальное переданное число *{max_num}*"


if __name__ == "__main__":
    app.run(debug=True)
