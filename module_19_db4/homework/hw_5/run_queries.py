import sqlite3

conn = sqlite3.connect("../homework.db")
cursor = conn.cursor()

with open("task5.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)
results = cursor.fetchall()

print("Анализ групп:")
print("Группа | Ученики | Средний балл | Не сдали | Просрочили | Повторные попытки")
print("-------|---------|--------------|----------|------------|------------------")

for group_id, total_students, avg_grade, not_submitted, overdue, retries in results:
    print(f"{group_id:6} | {total_students:7} | {avg_grade:.2f}        | {not_submitted:8} | {overdue:10} | {retries:16}")

conn.close()