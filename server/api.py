from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from decouple import config


app = FastAPI()

# --- Конфигурация БД ---

DB_CONFIG = {
    "dbname": config("DB_NAME"),
    "user": config("DB_USER"),
    "password": config("DB_PASSWORD"),
    "host": config("DB_HOST"),
    "port": config("DB_PORT")
}

def get_connection():
    return psycopg2.connect(cursor_factory=RealDictCursor, **DB_CONFIG)

# --- Модели ---
class UserRegister(BaseModel):
    username: str
    password: str
    phone: str

class UserLogin(BaseModel):
    username: str
    password: str

class MessageSend(BaseModel):
    sender: str
    content: str

class ChatCreate(BaseModel):
    user_id: int
    chat_name: str

# --- Эндпоинты ---
@app.post("/register")
def register(user: UserRegister):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (username, password, phone) VALUES (%s, %s, %s)
                """, (user.username, user.password, user.phone))
                conn.commit()
        return {"message": "Пользователь зарегистрирован"}
    except psycopg2.IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

@app.post("/login")
def login(user: UserLogin):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, username FROM users WHERE username = %s AND password = %s
            """, (user.username, user.password))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=401, detail="Неверные данные")
    return {"message": "Успешный вход", "user_id": result["id"], "username": result["username"]}


@app.post("/message")
def send_message(msg: MessageSend):
    # В будущем можно записывать сообщение в базу
    print(f"{msg.sender}: {msg.content}")
    return {"message": "Сообщение получено"}

@app.get("/chats/{user_id}")
def get_user_chats(user_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT chats.id, chats.name FROM chats
                JOIN chat_users ON chats.id = chat_users.chat_id
                WHERE chat_users.user_id = %s
            """, (user_id,))
            return cur.fetchall()

@app.post("/chats")
def create_chat(data: ChatCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chats (name) VALUES (%s) RETURNING id
            """, (data.chat_name,))
            chat_id = cur.fetchone()["id"]
            cur.execute("""
                INSERT INTO chat_users (chat_id, user_id) VALUES (%s, %s)
            """, (chat_id, data.user_id))
            conn.commit()
    return {"message": "Чат создан", "chat_id": chat_id}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)

