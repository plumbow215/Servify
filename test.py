import sqlite3

conn = sqlite3.connect("Servify.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM USERS WHERE USERNAME = ?", ("Plumbow",))
fetched = cursor.fetchone()

conn.close()

print(fetched[0])
