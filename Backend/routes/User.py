import sqlite3, os, bcrypt, json
import Backend.session as session
from fastapi import APIRouter, HTTPException
from datetime import datetime

DB_PATH = "Servify.db"

router = APIRouter(prefix="/users", tags = ["Users"])

# verifies login
@router.post("/verify-login")
async def verify_password(email: str, password: str):
    datenow = datetime.now().strftime('%d %b %Y')
    conn = sqlite3.connect("Servify.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch UserId, Email, Password, and Role from the database
    cursor.execute("SELECT UserId, email, password, role FROM USERS WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user_id, email, hashed_password, role = user  # Extract role from query result
    print(role)
    
    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        # Update lastActive date
        cursor.execute("UPDATE USERS SET lastActive = ? WHERE UserId = ?", (datenow, user_id))
        conn.commit()
        
        # Load session.json and update user_id & role
        with open("Backend/session.json", "r") as file:
            session_data = json.load(file)
        
        session_data["user_id"] = user_id
        session_data["role"] = role  # Store the role
        
        with open("Backend/session.json", "w") as file:
            json.dump(session_data, file, indent=4)
        
        # Fetch updated user details
        cursor.execute("SELECT * FROM USERS WHERE Email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        return {"User": "Credentials are matching!", "details": dict(user)}
    else:
        raise HTTPException(status_code=401, detail="Credentials don't match!")

# creates a new user
@router.post("/create-user")
async def CreateUser(username: str, email: str, password: str):
    datenow = datetime.now().strftime('%d %b %Y')
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM USERS WHERE EMAIL = ?", (email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already exists!")
    
    cursor.execute("""
                   INSERT INTO USERS (
                       username,
                       email,
                       password,
                       aboutMe,
                       creationDate,
                       lastActive,
                       services,
                       role
                   )
                   VALUES (?,?,?,?,?,?,?,?)
                   """, (username, email, hashed_password, "Placeholder", datenow, datenow, 0, "NULL"))
    conn.commit()
    
    cursor.execute("""SELECT UserId FROM USERS WHERE email = ?""", (email,))
    userid = cursor.fetchone()
    
    session_data = {"user_id": int(userid[0]), "event_id": 0, "role": "Volunteer"}
    with open("Backend/session.json", "w") as f:
        json.dump(session_data, f)
            
    conn.close()
    
    return {"User": "New user created"}  

@router.patch("/change-role")
async def change_role(UserId : int, role : str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""UPDATE USERS SET role = ? WHERE UserId = ?""", (role, UserId))
    conn.commit()
    conn.close()
    
    return {"User:" "Successfully updated user role"}
    
    
@router.patch("/update-registration")
async def update_registration(UserId: int):
    JSON_PATH = "Backend/registration.json"
    SESSION_PATH = "Backend/session.json"  # Store user_id here
    
    # Load data from JSON
    try:
        with open(JSON_PATH, "r") as f:
            registration_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Error loading registration.json")

    role = registration_data["role"]
    skills = registration_data["skills"]
    interests = registration_data["interests"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        #  Store UserId in session.json for later use
        with open(SESSION_PATH, "r") as f:
            session_data = json.load(f)
        
        #  Update the role in USERS table
        cursor.execute("UPDATE USERS SET role = ? WHERE UserId = ?", (role, UserId))

        #  Add skills if they don't already exist
        for skill in skills:
            cursor.execute("SELECT 1 FROM SKILLS WHERE UserId = ? AND skill = ?", (UserId, skill))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO SKILLS (UserId, skill) VALUES (?, ?)", (UserId, skill))

        #  Add interests if they don't already exist
        for interest in interests:
            cursor.execute("SELECT 1 FROM INTERESTS WHERE UserId = ? AND interest = ?", (UserId, interest))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO INTERESTS (UserId, interest) VALUES (?, ?)", (UserId, interest))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        conn.close()

    return {"message": "User registration data updated successfully"}
    

@router.patch("/update-services")
async def UpdateUserServices(userid: int):
    conn = sqlite3.connect("DB_PATH")
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM USERS WHERE UserId = ?
                   """, (userid))
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    
    return user

@router.patch("/update-activity")
async def UpdateUserLastActive(email: str):
    datenow = datetime.now().strftime('%d %b %Y')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE USERS
                   SET lastActive = ?
                   WHERE email = ? 
                   """, (datenow, email))
    conn.commit()
    conn.close()
    
    return {"User": "Successfully updated user's lastActive"}