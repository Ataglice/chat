import tkinter as tk
from tkinter import messagebox
from api_client import register_user, login_user

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login / Register")

        # Поля ввода
        tk.Label(root, text="Username").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Password").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Phone (only for registration)").grid(row=2, column=0, padx=5, pady=5)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(root, text="Login", command=self.login).grid(row=3, column=0, pady=10)
        tk.Button(root, text="Register", command=self.register).grid(row=3, column=1, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        response = login_user(username, password)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Login successful!")
            # Здесь можно открыть основное окно приложения
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()

        response = register_user(username, password, phone)
        if response.status_code == 200:
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Registration failed.")
