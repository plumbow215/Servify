from fastapi import APIRouter, Depends, HTTPException
import sqlite3
import Backend.session as session

router = APIRouter(prefix="/Profile", tags=["Profile"])

DB_PATH = "Servify.db"


async def get_current_user_UserId():
    user_UserId = session.get_user_UserId()
    if not user_UserId:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_UserId

# Get user profile by user UserId
@router.get("/{user_id}")
async def get_users_by_UserId(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE UserId = ?", (user_id,))
    profile = cursor.fetchone()
    conn.close()

    if profile is None:
        raise HTTPException(status_code=404, detail="users not found")

    return {"details": "successfully fetched", "user": [dict(profile)]}

# Delete
@router.delete("/{user_UserId}", response_model=dict)
async def delete_users(user_UserId: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE UserId = ?", (user_UserId,))
    conn.commit()
    conn.close()

    return {"message": "users deleted "}
