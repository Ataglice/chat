import psycopg2

DB_NAME = "chat"
DB_USER = "postgres"
DB_PASSWORD = "Lart8527"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

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

def check_credentials(username, password, phone):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s AND phone = %s",
                (username, password)
            )
            return cursor.fetchone() is not None
