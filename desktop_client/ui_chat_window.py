import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
import threading
import time

BASE_URL = "https://chat-0w96.onrender.com"

class ChatWindow(tk.Toplevel):
    def __init__(self, chat_id, user_id):
        super().__init__()
        self.chat_id = chat_id
        self.user_id = user_id
        self.stop_updating = False  # флаг для остановки потока при закрытии окна

        self.title(f"Чат {chat_id}")
        self.geometry("600x500")

        self.messages_text = tk.Text(self, state=tk.DISABLED)
        self.messages_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(padx=10, pady=5, fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.add_user_button = tk.Button(self, text="Добавить пользователя", command=self.add_user)
        self.add_user_button.pack(padx=10, pady=5)

        self.load_messages()

        # запускаем фоновый поток
        threading.Thread(target=self.auto_update_messages_thread, daemon=True).start()

        # обработка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_messages(self):
        try:
            response = requests.get(f"{BASE_URL}/messages/{self.chat_id}")
            if response.status_code == 200:
                messages = response.json()
                self.messages_text.config(state=tk.NORMAL)
                self.messages_text.delete(1.0, tk.END)

                for msg in messages:
                    text = f'[{msg["timestamp"]}] {msg["sender"]}: {msg["content"]}\n'
                    self.messages_text.insert(tk.END, text)

                self.messages_text.config(state=tk.DISABLED)
                self.messages_text.see(tk.END)  # автопрокрутка вниз
            else:
                # Можно вывести сообщение об ошибке, если захотите
                pass
        except requests.exceptions.RequestException:
            # Ошибки сети можно тихо игнорировать в фоне
            pass

    def send_message(self, event=None):
        content = self.entry.get()
        if not content.strip():
            return
        try:
            response = requests.post(f"{BASE_URL}/messages", json={
                "chat_id": int(self.chat_id),
                "sender_id": int(self.user_id),
                "content": content
            })
            if response.status_code == 200:
                self.entry.delete(0, tk.END)
                self.load_messages()
            else:
                messagebox.showerror("Ошибка", "Не удалось отправить сообщение")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен\n{e}")

    def add_user(self):
        identifier = simpledialog.askstring("Добавить пользователя", "Введите username или телефон:")
        if not identifier:
            return
        try:
            response = requests.post(f"{BASE_URL}/chats/{self.chat_id}/add_user", json={
                "identifier": identifier,
                "requester_id": self.user_id
            })
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Пользователь добавлен в чат")
            else:
                messagebox.showerror("Ошибка", response.json().get("detail", "Не удалось добавить пользователя"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен\n{e}")

    def auto_update_messages_thread(self):
        while not self.stop_updating:
            time.sleep(2)
            self.after(0, self.load_messages)

    def on_close(self):
        self.stop_updating = True
        self.destroy()
