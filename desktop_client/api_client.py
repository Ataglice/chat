import requests

BASE_URL = "https://chat-0w96.onrender.com"  # или твой Render URL

def register_user(username, password, phone):
    return requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password,
        "phone": phone
    })

def login_user(username, password):
    response = requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        data = response.json()
        return {
            "status": "ok",
            "user_id": data["user_id"],
            "username": data["username"]
        }
    else:
        return {
            "status": "error",
            "detail": response.json().get("detail")
        }
