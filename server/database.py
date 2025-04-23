import psycopg2
from decouple import config


DB_CONFIG = {
    "dbname": config("DB_NAME"),
    "user": config("DB_USER"),
    "password": config("DB_PASSWORD"),
    "host": config("DB_HOST"),
    "port": config("DB_PORT")
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def register_user(username, password, phone):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password, phone) VALUES (%s, %s, %s)",
                    (username, password, phone)
                )
                conn.commit()
                return True
    except psycopg2.IntegrityError:
        return False

def check_credentials(username, password):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password)
            )
            return cursor.fetchone() is not None
