import sqlite3

def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
            INSERT INTO table_users (username, password)
            VALUES ('{username}', '{password}');
            """
        )
        conn.commit()


def hack() -> None:
    # Пример 1: удаление таблицы
    username: str = "hacker"
    password: str = "badpass'); DROP TABLE table_users; --"
    register(username, password)

    # Пример 2: массовое добавление записей
    username2: str = "spammer"
    password2: str = "pw'); INSERT INTO table_users (username, password) VALUES ('bot1','123'); INSERT INTO table_users (username, password) VALUES ('bot2','456'); --"
    register(username2, password2)


#Защищённый вариант (для сравнения)
def safe_register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        # Используем параметризацию — инъекция не сработает
        cursor.execute(
            "INSERT INTO table_users (username, password) VALUES (?, ?);",
            (username, password)
        )
        conn.commit()


if __name__ == '__main__':
    register('wignorbo', 'sjkadnkjasdnui31jkdwq')
    hack()
    # safe_register('secure_user', 'strong_password')  # пример безопасного вызова
