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

def save_user_profile(username, email, password_hash, full_name=None, bio=None, profile_picture=None):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO user_profile (username, email, password_hash, full_name, bio, profile_picture, created_on)
    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"""
                   (username, email, password_hash, full_name, bio, profile_picture)
    )
conn.commit()
conn.close()

def get_user_profile_by_username(username):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile WHERE username = ?", (username))
    profile = cursor.fetchone()
    conn.close()
    return profile


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
