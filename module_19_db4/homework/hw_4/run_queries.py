import sqlite3

conn = sqlite3.connect("../homework.db")
cursor = conn.cursor()

with open("task4.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)
results = cursor.fetchall()

print("Среднее, максимальное и минимальное количество просроченных заданий для каждого класса:")
for group_id, avg_overdue, max_overdue, min_overdue in results:
    print(f"Класс {group_id}: среднее={avg_overdue:.2f}, макс={max_overdue}, мин={min_overdue}")

conn.close()