import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
from ui_chat_window import ChatWindow

BASE_URL = "http://127.0.0.1:8000"  # или твой Render URL

class ChatListWindow(tk.Tk):
    def __init__(self, user_id):
        super().__init__()
        self.title("Список чатов")
        self.geometry("400x400")
        self.user_id = user_id

        self.chat_listbox = tk.Listbox(self)
        self.chat_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_listbox.bind("<Double-Button-1>", self.open_chat)

        tk.Button(self, text="Создать чат", command=self.create_chat).pack(pady=5)

        self.load_chats()

    def load_chats(self):
        try:
            response = requests.get(f"{BASE_URL}/chats/{self.user_id}")
            if response.status_code == 200:
                chats = response.json()
                self.chat_listbox.delete(0, tk.END)
                for chat in chats:
                    self.chat_listbox.insert(tk.END, f'{chat["id"]}: {chat["name"]}')
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить чаты")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен\n{e}")

    def create_chat(self):
        name = simpledialog.askstring("Создать чат", "Введите имя чата:")
        if not name:
            return
        try:
            response = requests.post(f"{BASE_URL}/chats", json={
                "chat_name": name,
                "user_id": self.user_id
            })
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Чат создан")
                self.load_chats()
            else:
                messagebox.showerror("Ошибка", response.json().get("detail", "Не удалось создать чат"))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен\n{e}")

    def open_chat(self, event):
        selected = self.chat_listbox.get(self.chat_listbox.curselection())
        chat_id, chat_name = selected.split(": ", 1)
        ChatWindow(chat_id=chat_id, user_id=self.user_id, chat_name=chat_name)

