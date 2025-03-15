import sqlite3, os, bcrypt, json
import Backend.session as session
from fastapi import APIRouter, HTTPException
from datetime import datetime

DB_PATH = "Servify.db"

router = APIRouter(prefix="/users")

# verifies login
@router.post("/verify-login")
async def verify_password(email: str, password: str):
    conn = sqlite3.connect("Servify.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT USERID, EMAIL, PASSWORD FROM USERS WHERE EMAIL = ?", (email,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user == None:
        raise HTTPException(status_code=404, detail="User not found!")
    
    user_id , email, hashed_password = user
    
    if bcrypt.checkpw(password.encode(), hashed_password.encode()):
        with open("Backend/session.json", "w") as f:
            json.dump({"user_id": user_id}, f)
       
        
        return {"User": "Credentials are matching!"}
    else:
        raise HTTPException(status_code=401, detail="Credentials doesn't match!")

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
                       services
                   )
                   VALUES (?,?,?,?,?,?,?)
                   """, (username, email, hashed_password, "Placeholder", datenow, datenow, 0))
    conn.commit()
    conn.close()
    
    return {"User": "New user created"}  

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