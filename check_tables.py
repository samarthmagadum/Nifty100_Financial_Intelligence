import sqlite3

conn = sqlite3.connect("nifty100.db")   # use your database path
cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")

tables = cursor.fetchall()

print("Tables in Database:\n")
for table in tables:
    print(table[0])

conn.close()