from server.database import register_user, check_credentials
import socket
import threading
from shared.config import HOST, PORT
from server.client_handler import handle_client

clients = []

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[✓] Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients))
        thread.start()

if __name__ == "__main__":
    # init_db()  # больше не вызывается
    start_server()
