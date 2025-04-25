import tkinter as tk
from tkinter import simpledialog, messagebox

class ChatListWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat List")

        self.chat_listbox = tk.Listbox(master, width=50, height=20)
        self.chat_listbox.pack(pady=10)

        self.create_chat_button = tk.Button(master, text="Создать чат", command=self.create_chat)
        self.create_chat_button.pack()

        self.chat_listbox.bind("<Double-Button-1>", self.open_chat)

        # Здесь позже будет запрос к API для получения чатов
        self.load_chats()

    def load_chats(self):
        # Пока просто заглушка
        chats = ["Чат с Иваном", "Групповой чат"]
        for chat in chats:
            self.chat_listbox.insert(tk.END, chat)

    def create_chat(self):
        username = simpledialog.askstring("Создание чата", "Введите имя пользователя:")
        chat_name = simpledialog.askstring("Создание чата", "Введите название чата:")

        if username and chat_name:
            # Здесь будет вызов API для создания чата
            messagebox.showinfo("Чат создан", f"Чат '{chat_name}' с {username} создан.")

    def open_chat(self, event):
        selected_chat = self.chat_listbox.get(self.chat_listbox.curselection())
        # Здесь будет открытие окна переписки
        messagebox.showinfo("Открытие чата", f"Открыт чат: {selected_chat}")
