import sqlite3
import random

def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    """
    Генерирует команды и распределяет их по группам.
    В каждую группу: 1 сильная, 2 средние, 1 слабая.
    """

    cursor.execute("DELETE FROM uefa_commands;")
    cursor.execute("DELETE FROM uefa_draw;")

    levels = ["Сильная", "Средняя", "Средняя", "Слабая"]
    team_id = 1

    for group in range(1, number_of_groups + 1):
        for level in levels:
            team_name = f"Команда_{team_id}"
            country = f"Страна_{team_id}"

            cursor.execute(
                "INSERT INTO uefa_commands (id, name, country, level) VALUES (?, ?, ?, ?);",
                (team_id, team_name, country, level)
            )

            cursor.execute(
                "INSERT INTO uefa_draw (team_id, group_id) VALUES (?, ?);",
                (team_id, group)
            )

            team_id += 1