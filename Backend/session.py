import json

def get_user_id():
    with open("Backend/session.json", "r") as f:
        data = json.load(f)
        return data.get("user_id")
    
def get_event_id():
    with open("Backend/session.json", "r") as f:
        data = json.load(f)
        return data.get("event_id")