from shared.config import BUFFER_SIZE
from server.broadcast import broadcast
from server.auth import process_auth  
import threading

def handle_client(client_socket, addr, clients):
    print(f"[+] Подключён: {addr}")

    # 🔐 Авторизация
    username = process_auth(client_socket)
    if not username:
        print(f"[!] Не удалось авторизовать {addr}")
        client_socket.close()
        return

    welcome_message = f"{username} присоединился к чату.\n".encode()
    broadcast(welcome_message, client_socket, clients)

    while True:
        try:
            message = client_socket.recv(BUFFER_SIZE)
            if not message:
                break
            full_message = f"{username}: {message.decode()}".encode()
            broadcast(full_message, client_socket, clients)
        except:
            break

    print(f"[-] Отключён: {addr}")
    clients.remove(client_socket)
    client_socket.close()

    goodbye = f"{username} вышел из чата.\n".encode()
    broadcast(goodbye, client_socket, clients)
