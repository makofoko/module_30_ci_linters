from flask import Flask
from datetime import datetime
import sys

app = Flask(__name__)

weekdays = (
    "понедельника",
    "вторника",
    "среды",
    "четверга",
    "пятницы",
    "субботы",
    "воскресенья",
)

@app.route("/hello-world/<name>")
def hello_world(name: str) -> str:
    """
    Endpoint, который возвращает приветствие с учётом текущего дня недели.
    """
    weekday_index = datetime.today().weekday()
    weekday_name = weekdays[weekday_index]
    return f"Привет, {name}. Хорошего {weekday_name}!"


if __name__ == "__main__":
    print("tuple:", sys.getsizeof(weekdays))
    print("list:", sys.getsizeof(list(weekdays)))
    print("dict:", sys.getsizeof({i: day for i, day in enumerate(weekdays)}))

    app.run(debug=True)
