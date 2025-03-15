import json

def get_user_id():
    with open("session.json", "r") as f:
        data = json.load(f)
        return data.get("user_id")