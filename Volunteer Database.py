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

def init_community_service_db():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_service_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            organizer TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_community_service_listing(title, description, date, location, organizer):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO community_service_listings (title, description, date, location, organizer) 
        VALUES (?, ?, ?, ?, ?)
    """, (title, description, date, location, organizer))
    conn.commit()
    conn.close()

def get_community_service_listings():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM community_service_listings")
    listings = cursor.fetchall()
    conn.close()
    return listings

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

def get_all_user_profiles():
    conn = sqlite3.connect(volunteers.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile")
    profiles = cursor.fetchall()
    conn.close()
    return profiles
                           
if __name__ == "__main__":
    init_db()
    init_community_service_db()
    print("Database initialized successfully.")
