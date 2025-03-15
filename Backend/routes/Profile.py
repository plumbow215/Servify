from fastapi import APIRouter, Depends, HTTPException
import sqlite3
import Backend.session as session

router = APIRouter(prefix="/Profile")

DB_PATH = "Servify.db"


async def get_current_user_UserId():
    user_UserId = session.get_user_UserId()
    if not user_UserId:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_UserId

# Get user profile by user UserId
@router.get("/{user_UserId}", response_model=dict)
async def get_users_by_UserId(user_UserId: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE UserId = ?", (user_UserId,))
    profile = cursor.fetchone()
    conn.close()

    if profile is None:
        raise HTTPException(status_code=404, detail="users not found")

    return {
        "UserId": profile[0],
        "username": profile[1],
        "email": profile[2],
        "password_hash": profile[3],
        "full_name": profile[4],
        "bio": profile[5],
        "profile_picture": profile[6],
        "created_on": profile[7],
    }

# Get current user's profile
@router.get("/me", response_model=dict)
async def get_current_users(user_UserId: int = Depends(get_current_user_UserId)):
    return get_users_by_UserId(user_id)

# Get all
@router.get("/", response_model=list[dict])
async def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    profiles = cursor.fetchall()
    conn.close()

    return [
        {
            "UserId": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
            "full_name": row[4],
            "bio": row[5],
            "profile_picture": row[6],
            "created_on": row[7],
        }
        for row in profiles
    ]

# Create
@router.post("/", response_model=dict)
async def create_users(
    username: str,
    email: str,
    password_hash: str,
    full_name: str = None,
    bio: str = None,
    profile_picture: str = None,
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users (username, email, password_hash, full_name, bio, profile_picture, created_on)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (username, email, password_hash, full_name, bio, profile_picture),
    )
    conn.commit()
    conn.close()

    return {"message": "users created"}

# Update
@router.put("/{user_UserId}", response_model=dict)
async def update_users(
    user_UserId: int,
    username: str = None,
    email: str = None,
    password_hash: str = None,
    full_name: str = None,
    bio: str = None,
    profile_picture: str = None,
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    updates = []
    params = []
    if username:
        updates.append("username = ?")
        params.append(username)
    if email:
        updates.append("email = ?")
        params.append(email)
    if password_hash:
        updates.append("password_hash = ?")
        params.append(password_hash)
    if full_name:
        updates.append("full_name = ?")
        params.append(full_name)
    if bio:
        updates.append("bio = ?")
        params.append(bio)
    if profile_picture:
        updates.append("profile_picture = ?")
        params.append(profile_picture)

    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")

    query = f"UPDATE users SET {', '.join(updates)} WHERE UserId = ?"
    params.append(user_UserId)

    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return {"message": "users updated "}

# Delete
@router.delete("/{user_UserId}", response_model=dict)
async def delete_users(user_UserId: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE UserId = ?", (user_UserId,))
    conn.commit()
    conn.close()

    return {"message": "users deleted "}
