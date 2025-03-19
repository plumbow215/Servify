import sqlite3, json
import Backend.session as session
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

DB_PATH = "Servify.db"
router = APIRouter(prefix="/community-service", tags=["Community Service"])

class CommunityListing(BaseModel):
    title: str
    description: str
    date: str 
    location: str
    organizer: str

def get_listing_by_id(event_id: int):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENTS WHERE EventId = ?", (event_id,))
    listing = cursor.fetchone()
    conn.close()
    
    if not listing:
        raise HTTPException(status_code=404, detail=f"Listing with ID {event_id} not found.")
    
    return listing[0]

@router.post("/create_event")
async def create_event():
    try:
        # Load event data from JSON file
        with open("Backend/event_data.json", "r") as file:
            event_data = json.load(file)

        # Load user session
        with open("Backend/session.json", "r") as file:
            session_data = json.load(file)

        user_id = session_data["user_id"]

        # Connect to the database
        conn = sqlite3.connect("Servify.db")
        cursor = conn.cursor()

        # Retrieve username from USERS table
        cursor.execute("SELECT username FROM USERS WHERE UserId = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        publisher = user[0]  # Extract username

        # Extract event data
        title = event_data["title"]
        venue = event_data["venue"]
        description = event_data["description"]  # Convert list to string
        date = event_data["date"]  # Already formatted as "17 Mar 2025"
        theme = event_data["selected_theme"]
        max_participants = event_data["maxParticipants"]
        status = "Active"
        published_since = datetime.now().strftime("%d %b %Y")
        curr_participants = 0

        # Insert into EVENTS table
        cursor.execute("""
            INSERT INTO EVENTS (title, description, date, venue, status, publisher, publisherId, publishedSince, currParticipants, maxParticipants, theme)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, description, date, venue, status, publisher, user_id, published_since, curr_participants, max_participants, theme))

        # Get the last inserted EventId
        event_id = cursor.lastrowid

        # Insert selected skills into EVENTSKILLS table
        for skill in event_data["selected_skills"]:
            cursor.execute("""
                INSERT INTO EVENTSKILLS (EventId, skill)
                VALUES (?, ?)
            """, (event_id, skill))

        # Commit changes and close connection
        conn.commit()
        conn.close()

        return {"message": "Event created successfully!", "event_id": event_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-listings")
async def get_listings():
    conn = sqlite3.connect("Servify.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENTS")
    listings = cursor.fetchall()
    
    if not listings:
        raise HTTPException(status_code=400, detail="Failed to get all events.")
    
    return {"details": "successfully fetched", "events": [dict(row) for row in listings]}

@router.get("/show-listing")
async def show_listing(EventId : int):
    conn = sqlite3.connect("Servify.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM EVENTS WHERE EventId = ?", (EventId,))
    event = cursor.fetchone()
    
    if not event:
        raise HTTPException(status_code=400, detail="Failed to get event.")
    
    return {"details": "successfully fetched", "event": [dict(event)]}


# @router.patch("/update-listing/{EventId}")
# async def update_listing(EventId: int, title: str, description: str, date: str, location: str):
#     listing = get_listing_by_id(EventId)

#     updated_values = {
#         "title": title if title else listing[1],
#         "description": description if description else listing[2],
#         "date": date if date else listing[3],
#         "location": location if location else listing[4],
#     }

#     db_execute("""
#         UPDATE EVENTS
#         SET title = ?, description = ?, date = ?, location = ?, updated_at = ?
#         WHERE EventId = ?
#     """, (updated_values["title"], updated_values["description"], updated_values["date"], updated_values["location"], datetime.now().strftime('%d %b %Y'), EventId))

#     return {"message": "Listing updated successfully", "EventId": EventId, "updated_data": updated_values}

# @router.delete("/delete-listing/{event_id}")
# async def delete_listing(event_id: int):
#     get_listing_by_id(event_id)

#     db_execute("DELETE FROM EVENTS WHERE EventId = ?", (event_id,))
#     return {"message": "Listing deleted successfully", "event_id": event_id}

# @router.get("/find-listing")
# async def find_listing(title: str = None, location: str = None, date: str = None):
#     if not any([title, location, date]):
#         raise HTTPException(status_code=400, detail="Provide at least one search parameter.")

#     query = "SELECT * FROM EVENTS WHERE"
#     conditions = []
#     params = []

#     if title:
#         conditions.append("title LIKE ?")
#         params.append(f"%{title}%")
#     if location:
#         conditions.append("location LIKE ?")
#         params.append(f"%{location}%")
#     if date:
#         conditions.append("date = ?")
#         params.append(date)

#     listings = db_execute(query + " AND ".join(conditions), params, fetch=True)
#     if not listings:
#         raise HTTPException(status_code=404, detail="No matching listings found.")

#     return [{"event_id": row[0], "title": row[1], "description": row[2], "date": row[3], "location": row[4], "organizer": row[5]} for row in listings]
