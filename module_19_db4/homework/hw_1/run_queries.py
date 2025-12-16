import sqlite3

conn = sqlite3.connect("homework.db")
cursor = conn.cursor()

with open("task1.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
    print(row)

conn.close()
