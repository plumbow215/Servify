from fastapi import APIRouter, Depends, HTTPException
import sqlite3
import Backend.session as session

router = APIRouter(prefix="/Profile")

DB_PATH = "Servify.db"


async def get_current_user_id():
    user_id = session.get_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id

# Get user profile by user ID
@router.get("/{user_id}", response_model=dict)
async def get_user_profile_by_id(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile WHERE id = ?", (user_id,))
    profile = cursor.fetchone()
    conn.close()

    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")

    return {
        "id": profile[0],
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
async def get_current_user_profile(user_id: int = Depends(get_current_user_id)):
    return get_user_profile_by_id(user_id)

# Get all
@router.get("/", response_model=list[dict])
async def get_all_user_profiles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile")
    profiles = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
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
async def create_user_profile(
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
        INSERT INTO user_profile (username, email, password_hash, full_name, bio, profile_picture, created_on)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        """,
        (username, email, password_hash, full_name, bio, profile_picture),
    )
    conn.commit()
    conn.close()

    return {"message": "User profile created"}

# Update
@router.put("/{user_id}", response_model=dict)
async def update_user_profile(
    user_id: int,
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

    query = f"UPDATE user_profile SET {', '.join(updates)} WHERE id = ?"
    params.append(user_id)

    cursor.execute(query, params)
    conn.commit()
    conn.close()

    return {"message": "User profile updated "}

# Delete
@router.delete("/{user_id}", response_model=dict)
async def delete_user_profile(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_profile WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return {"message": "User profile deleted "}
