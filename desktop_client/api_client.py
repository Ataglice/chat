import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user(username, password, phone):
    return requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password,
        "phone": phone
    })

def login_user(username, password):
    return requests.post(f"{BASE_URL}/login", json={
        "username": username,
        "password": password
    })
