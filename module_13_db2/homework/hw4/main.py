import sqlite3

IVAN_SOVIN_SALARY = 100000

def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    """
    Повышает зарплату сотрудника на 10% или увольняет его,
    если она превысит зарплату Ивана Совина.
    """
    cursor.execute(
        "SELECT salary FROM table_effective_manager WHERE name = ?;",
        (name,)
    )
    row = cursor.fetchone()

    if row is None:
        print(f"Сотрудник {name} не найден.")
        return

    current_salary = row[0]

    if name == "Иван Совин":
        print("Эффективный менеджер не увольняется и не меняет зарплату.")
        return

    new_salary = int(current_salary * 1.1)

    if new_salary > IVAN_SOVIN_SALARY:
        cursor.execute(
            "DELETE FROM table_effective_manager WHERE name = ?;",
            (name,)
        )
        print(f"Сотрудник {name} уволен.")
    else:
        cursor.execute(
            "UPDATE table_effective_manager SET salary = ? WHERE name = ?;",
            (new_salary, name)
        )
        print(f"Зарплата сотрудника {name} повышена до {new_salary}.")