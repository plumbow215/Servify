from fastapi import APIRouter, Depends
import sqlite3
import Backend.session as session

router = APIRouter(prefix="/BookmarkedServices")

DB_PATH = "Servify.db"

def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/save")
def save_bookmarked_service_record(
    date: str, venue: str, volunteeredOn: str, createdOn: str, publisher: str, 
    user_id: int = Depends(session.get_user_id)  # Get user_id from session
):
    """Saves a bookmarked service record for the logged-in user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookmarked_service_records (user_id, date, venue, volunteeredOn, createdOn, publisher) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date, venue, volunteeredOn, createdOn, publisher))
    conn.commit()
    conn.close()
    return {"message": "Bookmarked service record saved successfully", "user_id": user_id}

@router.get("/get")
def get_bookmarked_service_records(user_id: int = Depends(session.get_user_id)):
    """Fetches bookmarked service records for the logged-in user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookmarked_service_records WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()
    conn.close()
    return {"user_id": user_id, "bookmarked_services": [dict(record) for record in records]}

@router.get("/get-bookmarkedservices")
def get_bookmarkedservices(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookmarked_service_records WHERE user_id = ?", (user_id,))
    records = cursor.fetchall()
    conn.close()
    
    return {"status": "f"}
