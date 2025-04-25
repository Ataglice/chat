import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

BASE_URL = "http://127.0.0.1:8000"  # или свой адрес

class ChatWindow(tk.Toplevel):
    def __init__(self, chat_id, user_id, chat_name=""):
        super().__init__()
        self.title(f"Чат: {chat_name or chat_id}")
        self.geometry("500x500")
        self.chat_id = chat_id
        self.user_id = user_id

        self.chat_display = scrolledtext.ScrolledText(self, state='disabled', wrap='word')
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self)
        self.entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.entry.bind("<Return>", self.send_message)

        tk.Button(self, text="Отправить", command=self.send_message).pack(pady=(0, 10))

        self.load_messages()

    def load_messages(self):
        # Заглушка, позже заменим на запрос к API
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, "История сообщений пока не реализована\n")
        self.chat_display.config(state='disabled')

    def send_message(self, event=None):
        content = self.entry.get()
        if not content.strip():
            return

        try:
            response = requests.post(f"{BASE_URL}/message", json={
                "sender": str(self.user_id),
                "content": content,
            })
            if response.status_code == 200:
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, f"Вы: {content}\n")
                self.chat_display.config(state='disabled')
                self.entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Не удалось отправить сообщение")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Сервер недоступен\n{e}")
