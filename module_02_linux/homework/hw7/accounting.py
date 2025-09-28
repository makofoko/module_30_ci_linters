from flask import Flask

app = Flask(__name__)

storage: dict[int, dict] = {}


@app.route("/add/<date>/<int:number>")
def add_expense(date: str, number: int) -> str:
    """
    Добавляет трату за конкретный день.
    Формат даты: YYYYMMDD
    """
    year = int(date[:4])
    month = int(date[4:6])

    storage.setdefault(year, {}).setdefault("total", 0)
    storage[year].setdefault(month, 0)

    storage[year]["total"] += number
    storage[year][month] += number

    return f"Добавлена трата {number} руб. за {date}"


@app.route("/calculate/<int:year>")
def calculate_year(year: int) -> str:
    """
    Возвращает суммарные траты за указанный год.
    """
    if year not in storage:
        return f"За {year} год трат не найдено."
    return f"Суммарные траты за {year} год: {storage[year]['total']} руб."


@app.route("/calculate/<int:year><int:month>")
def calculate_month(year: int, month: int) -> str:
    """
    Возвращает суммарные траты за указанный год и месяц.
    """
    if year not in storage or month not in storage[year]:
        return f"За {month:02d}.{year} трат не найдено."
    return f"Суммарные траты за {month:02d}.{year}: {storage[year][month]} руб."


if __name__ == "__main__":
    app.run(debug=True)
