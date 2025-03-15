from pydantic import BaseModel
from datetime import datetime

class CreateUser(BaseModel):
    # important stuff
    username: str
    email: str
    password: str
    
    # descriptive attributes
    aboutMe: str = "Tell us about yourself!"
    creationDate: str = datetime.now().strftime('%d %b %Y')
    lastActive: str = datetime.now().strftime('%d %b %Y')
    services: int = 0
    