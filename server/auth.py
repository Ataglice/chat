from server.database import register_user, check_credentials

def process_auth(client_socket):
    """
    Отправляет клиенту меню входа/регистрации и обрабатывает выбор.
    Возвращает имя пользователя при успехе, иначе None.
    """
    try:
        client_socket.send("1 - Войти\n2 - Зарегистрироваться\nВыберите: ".encode())
        choice = client_socket.recv(1024).decode().strip()

        client_socket.send("Логин: ".encode())
        username = client_socket.recv(1024).decode().strip()

        client_socket.send("Пароль: ".encode())
        password = client_socket.recv(1024).decode().strip()

        client_socket.send("Телефон: ".encode())
        phone = client_socket.recv(1024).decode().strip()

        if choice == "1":
            if check_credentials(username, password):
                client_socket.send(f"[✓] Успешный вход, {username}!\n".encode())
                return username
            else:
                client_socket.send("[!] Неверный логин или пароль.\n".encode())
                return None

        elif choice == "2":
            if register_user(username, password, phone):
                client_socket.send(f"[✓] Регистрация прошла успешно, {username}!\n".encode())
                return username
            else:
                client_socket.send("[!] Пользователь уже существует.\n".encode())
                return None

        else:
            client_socket.send("[!] Неверный выбор.\n".encode())
            return None

    except Exception as e:
        client_socket.send(f"[!] Ошибка авторизации: {e}\n".encode())
        return None