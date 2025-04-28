import requests

BASE_URL = "https://chat-0w96.onrender.com"  

def register_user(username, password, phone):
    return requests.post(f"{BASE_URL}/register", json={
        "username": username,
        "password": password,
        "phone": phone
    })

def login_user(username, password):
    try:
        response = requests.post(f"{BASE_URL}/login", json={
            "username": username,
            "password": password
        }, timeout=10)  # timeout на всякий случай

        if response.status_code == 200:
            data = response.json()
            return {
                "status": "ok",
                "user_id": data["user_id"],
                "username": data["username"]
            }
        else:
            try:
                error_data = response.json()
                detail = error_data.get("detail", "Неизвестная ошибка")
            except requests.exceptions.JSONDecodeError:
                detail = "Сервер вернул некорректный ответ"

            return {
                "status": "error",
                "detail": detail
            }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "detail": f"Ошибка соединения с сервером: {e}"
        }

