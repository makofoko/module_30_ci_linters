import datetime
import sqlite3


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    """
    Добавляет новую птицу в таблицу table_birds.
    """
    cursor.execute(
        "INSERT INTO table_birds (time_observed, bird_name) VALUES (?, ?);",
        (date_time, bird_name)
    )


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    """
    Проверяет, наблюдалась ли такая птица ранее.
    Использует выборку с условием и не получает все записи.
    """
    cursor.execute(
        "SELECT 1 FROM table_birds WHERE bird_name = ? LIMIT 1;",
        (bird_name,)
    )
    return cursor.fetchone() is not None


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")
        connection.commit()