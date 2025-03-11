import sqlite3

def init_db():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            contact TEXT NOT NULL,
            skills TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_volunteer(name, age, contact, skills):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO volunteers (name, age, contact, skills) VALUES (?, ?, ?, ?)", 
                   (name, age, contact, skills))
    conn.commit()
    conn.close()

def get_volunteers():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM volunteers")
    volunteers = cursor.fetchall()
    conn.close()
    return volunteers

def save_bookmarked_service_record(date, venue, volunteeredOn, createdOn, publisher):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookmarked_service_records (date, venue, volunteeredOn, createdOn, publisher) 
        VALUES (?, ?, ?, ?, ?)
    """, (date, venue, volunteeredOn, createdOn, publisher))
    conn.commit()
    conn.close()

def get_bookmarked_service_records():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookmarked_service_records")
    records = cursor.fetchall()
    conn.close()
    return records

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
