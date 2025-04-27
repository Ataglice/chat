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

class MessageCreate(BaseModel):
    chat_id: int
    sender_id: int
    content: str

class MessageRead(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    timestamp: str

class AddUserByIdentifier(BaseModel):
    identifier: str  # username или phone
    requester_id: int  # id того, кто вызывает добавление


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

@app.post("/messages")
def create_message(message: MessageCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (chat_id, sender_id, content) VALUES (%s, %s, %s) RETURNING id, chat_id, sender_id, content, timestamp
            """, (message.chat_id, message.sender_id, message.content))
            result = cur.fetchone()
            conn.commit()
    return result


@app.get("/messages/{chat_id}")
def get_messages(chat_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, chat_id, sender_id, content, timestamp FROM messages
                WHERE chat_id = %s ORDER BY timestamp ASC
            """, (chat_id,))
            return cur.fetchall()


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

@app.post("/chats/{chat_id}/add_user")
def add_user_to_chat(chat_id: int, data: AddUserByIdentifier):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Ищем пользователя по username или телефону
            cur.execute("""
                SELECT id FROM users WHERE username = %s OR phone = %s
            """, (data.identifier, data.identifier))
            user = cur.fetchone()
            if not user:
                raise HTTPException(status_code=404, detail="Пользователь не найден")

            user_id = user["id"]
            
            # Проверяем: пытаемся ли добавить самого себя
            if user_id == data.requester_id:
                raise HTTPException(status_code=400, detail="Нельзя добавить самого себя в чат")

            # Проверяем, не состоит ли он уже в чате
            cur.execute("""
                SELECT 1 FROM chat_users WHERE chat_id = %s AND user_id = %s
            """, (chat_id, user_id))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Пользователь уже в чате")

            # Добавляем пользователя
            cur.execute("""
                INSERT INTO chat_users (chat_id, user_id) VALUES (%s, %s)
            """, (chat_id, user_id))
            conn.commit()
    return {"message": "Пользователь добавлен в чат"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)

