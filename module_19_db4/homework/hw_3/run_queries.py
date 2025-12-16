import sqlite3

conn = sqlite3.connect("../homework.db")
cursor = conn.cursor()

with open("task3.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)
results = cursor.fetchall()

print("Ученики преподавателя с самыми простыми заданиями:")
for row in results:
    print(row[0])

conn.close()