from flask import Flask
import os

app = Flask(__name__)


@app.route("/head_file/<int:size>/<path:relative_path>")
def head_file(size: int, relative_path: str) -> str:
    """
    Endpoint, который возвращает превью файла:
    - абсолютный путь и количество реально прочитанных символов
    - первые SIZE символов файла
    """
    abs_path = os.path.abspath(relative_path)

    if not os.path.exists(abs_path):
        return f"Ошибка: файл {abs_path} не найден."

    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            result_text = f.read(size)  
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"

    result_size = len(result_text)

    return f"<b>{abs_path}</b> {result_size}<br>{result_text}"


if __name__ == "__main__":
    app.run(debug=True)

