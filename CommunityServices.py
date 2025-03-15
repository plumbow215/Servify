import sqlite3
import Backend.session as session
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime

DB_PATH = "Servify.db"
router = APIRouter(prefix="/community-service", tags=["Community Service"])

print("Community Service Router Loaded Successfully")

class CommunityListing(BaseModel):
    title: str
    description: str
    date: str 
    location: str
    organizer: str

def db_execute(query, params=(), fetch=False):
    """Handles database operations safely with error handling."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall() if fetch else None
        conn.commit()
        return data
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database operation failed: {str(e)}")
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Data integrity error (e.g., duplicate entry).")
    finally:
        conn.close()

def get_listing_by_id(event_id: int):
    listing = db_execute("SELECT * FROM EVENTS WHERE event_id = ?", (event_id,), fetch=True)
    if not listing:
        raise HTTPException(status_code=404, detail=f"Listing with ID {event_id} not found.")
    return listing[0]

@router.post("/create-listing", response_model=CommunityListing)
async def create_listing(listing: CommunityListing):
    existing = db_execute("SELECT 1 FROM EVENTS WHERE title = ? AND date = ?", 
                          (listing.title, listing.date), fetch=True)
    if existing:
        raise HTTPException(status_code=400, detail="A listing with the same title and date already exists.")

    db_execute("""
        INSERT INTO EVENTS (title, description, date, location, organizer, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (listing.title, listing.description, listing.date, listing.location, listing.organizer, datetime.now().strftime('%d %b %Y')))

    return listing

@router.get("/listings")
async def get_listings():
    listings = db_execute("SELECT * FROM EVENTS", fetch=True)
    if not listings:
        raise HTTPException(status_code=404, detail="No community service listings found.")
    
    return [{"event_id": row[0], "title": row[1], "description": row[2], "date": row[3], "location": row[4], "organizer": row[5]} for row in listings]

@router.patch("/update-listing/{event_id}")
async def update_listing(event_id: int, title: str = None, description: str = None, date: str = None, location: str = None):
    listing = get_listing_by_id(event_id)

    updated_values = {
        "title": title if title else listing[1],
        "description": description if description else listing[2],
        "date": date if date else listing[3],
        "location": location if location else listing[4],
    }

    db_execute("""
        UPDATE EVENTS
        SET title = ?, description = ?, date = ?, location = ?, updated_at = ?
        WHERE event_id = ?
    """, (updated_values["title"], updated_values["description"], updated_values["date"], updated_values["location"], datetime.now().strftime('%d %b %Y'), event_id))

    return {"message": "Listing updated successfully", "event_id": event_id, "updated_data": updated_values}

@router.delete("/delete-listing/{event_id}")
async def delete_listing(event_id: int):
    get_listing_by_id(event_id)

    db_execute("DELETE FROM EVENTS WHERE event_id = ?", (event_id,))
    return {"message": "Listing deleted successfully", "event_id": event_id}

@router.get("/find-listing")
async def find_listing(title: str = None, location: str = None, date: str = None):
    if not any([title, location, date]):
        raise HTTPException(status_code=400, detail="Provide at least one search parameter.")

    query = "SELECT * FROM EVENTS WHERE"
    conditions = []
    params = []

    if title:
        conditions.append("title LIKE ?")
        params.append(f"%{title}%")
    if location:
        conditions.append("location LIKE ?")
        params.append(f"%{location}%")
    if date:
        conditions.append("date = ?")
        params.append(date)

    listings = db_execute(query + " AND ".join(conditions), params, fetch=True)
    if not listings:
        raise HTTPException(status_code=404, detail="No matching listings found.")

    return [{"event_id": row[0], "title": row[1], "description": row[2], "date": row[3], "location": row[4], "organizer": row[5]} for row in listings]
