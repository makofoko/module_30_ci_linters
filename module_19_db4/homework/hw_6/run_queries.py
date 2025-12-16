import sqlite3

conn = sqlite3.connect("../homework.db")
cursor = conn.cursor()

with open("task6.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)
result = cursor.fetchone()

print("Средняя оценка за задания, где нужно было что-то прочитать и выучить:")

if result and result[0] is not None:
    print(f"{result[0]:.2f}")
else:
    print("Нет заданий с условием 'прочитать/выучить'")

conn.close()