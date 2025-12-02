import sqlite3

with sqlite3.connect("hw_4_database.db") as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM salaries WHERE salary < 5000;")
    poor_count = cursor.fetchone()[0]
    print("За чертой бедности:", poor_count)

    cursor.execute("SELECT AVG(salary) FROM salaries;")
    avg_salary = cursor.fetchone()[0]
    print("Средняя зарплата:", round(avg_salary, 2))

    cursor.execute("SELECT COUNT(*) FROM salaries;")
    total = cursor.fetchone()[0]

    if total % 2 == 1:
        cursor.execute("""
            SELECT salary FROM salaries
            ORDER BY salary
            LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2;
        """)
        median_salary = cursor.fetchone()[0]
    else:
        cursor.execute("""
            SELECT AVG(salary) FROM (
                SELECT salary FROM salaries
                ORDER BY salary
                LIMIT 2 OFFSET ((SELECT COUNT(*) FROM salaries) / 2 - 1)
            );
        """)
        median_salary = cursor.fetchone()[0]

    print("Медианная зарплата:", median_salary)

    cursor.execute("""
        WITH total AS (
            SELECT COUNT(*) AS cnt FROM salaries
        ),
        top10 AS (
            SELECT SUM(salary) AS sum_top
            FROM salaries
            ORDER BY salary DESC
            LIMIT (SELECT CAST(cnt*0.1 AS INT) FROM total)
        ),
        rest90 AS (
            SELECT SUM(salary) AS sum_rest
            FROM salaries
            ORDER BY salary ASC
            LIMIT (SELECT CAST(cnt*0.9 AS INT) FROM total)
        )
        SELECT ROUND(100.0 * (SELECT sum_top FROM top10) / (SELECT sum_rest FROM rest90), 2);
    """)
    inequality_F = cursor.fetchone()[0]
    print("Число социального неравенства F:", f"{inequality_F}%")