import sqlite3
import csv

def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    """
    Удаляет ошибочные штрафы из таблицы table_fees.
    Сравнение происходит по дате и номеру автомобиля.
    """
    with open(wrong_fees_file, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            date, car_number = row
            cursor.execute(
                "DELETE FROM table_fees WHERE date = ? AND car_number = ?;",
                (date, car_number)
            )

