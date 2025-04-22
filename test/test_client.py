import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break

def send_messages(sock):
    while True:
        try:
            message = input()
            if message:
                sock.send(message.encode())
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"[✓] Подключено к серверу {HOST}:{PORT}")

    # 🔄 Получаем приглашения на ввод логина/пароля и отправляем ответы
    def handle_auth():
        while True:
            data = sock.recv(1024).decode()
            print(data, end="")

            # если в приглашении просят ввести что-то — ждём ввода
            if any(keyword in data.lower() for keyword in ["выберите", "логин", "пароль"]):
                response = input()
                sock.send(response.encode())

            if "[✓]" in data or "[!]" in data:
                # если успешный вход или неуспех — завершаем цикл
                break


    handle_auth()

    # 📥 Поток на приём сообщений
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    # 📤 Отправка сообщений
    send_messages(sock)

if __name__ == "__main__":
    main()
