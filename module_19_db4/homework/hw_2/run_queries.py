import sqlite3

conn = sqlite3.connect("../homework.db")
cursor = conn.cursor()

with open("task2.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)
results = cursor.fetchall()

print("Топ-10 лучших учеников по среднему баллу:")
for full_name, avg_grade in results:
    print(f"{full_name}: {avg_grade:.2f}")

conn.close()