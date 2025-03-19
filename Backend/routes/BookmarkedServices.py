from fastapi import APIRouter, Depends, HTTPException
import sqlite3
import Backend.session as session

router = APIRouter(prefix="/BookmarkedServices", tags=["Bookmarked Services"])

DB_PATH = "Servify.db"

def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.post("/save-userevent")
def save_userevent(UserId : int, EventId : int):
    """Saves a bookmarked service record for the logged-in user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # changes made by ethan
    # check if user exists
    cursor.execute("""SELECT 1 FROM USERS WHERE UserId = ?""", (UserId,))
    User = cursor.fetchone()
    if not User:
        raise HTTPException(status_code=404, detail="User does not exist!")
    
    # check if event exists
    cursor.execute("""SELECT 1 FROM EVENTS WHERE EventId = ?""", (EventId,))
    Event = cursor.fetchone()
    if not Event:
        raise HTTPException(status_code=404, detail="Event does not exist!")
    
    # check if user has already joined this event
    cursor.execute("""SELECT 1 FROM USEREVENTS WHERE UserId = ? AND EventId = ?""", (UserId, EventId))
    already_bookmarked = cursor.fetchone()
    if already_bookmarked:
        raise HTTPException(status_code=400, detail="Event already bookmarked!")
    
    cursor.execute("""
        INSERT INTO USEREVENTS (UserId, EventId) 
        VALUES (?, ?)
    """, (UserId, EventId))
    
    conn.commit()
    conn.close()
    
    return {"message": "Bookmarked service record saved successfully"}

@router.get("/get-userevents")
def get_userevents(UserId: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USEREVENTS WHERE UserId= ?", (UserId,))
    records = cursor.fetchall()
    conn.close()
    return {"bookmarked_services": [record["EventId"] for record in records]}