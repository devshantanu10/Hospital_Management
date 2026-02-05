import tkinter as tk
from tkinter import messagebox
import admin

USERNAME = "admin"
PASSWORD = "1234"

def login():
    if username.get() == USERNAME and password.get() == PASSWORD:
        root.destroy()
        admin.open_admin()
    else:
        messagebox.showerror("Error", "Invalid login credentials")

root = tk.Tk()
root.title("Hospital Management System - Login")
root.geometry("400x300")
root.configure(bg="#e3f2fd")

tk.Label(root, text="Login", font=("Arial", 20, "bold"), bg="#e3f2fd").pack(pady=20)

tk.Label(root, text="Username", bg="#e3f2fd").pack()
username = tk.Entry(root)
username.pack()

tk.Label(root, text="Password", bg="#e3f2fd").pack()
password = tk.Entry(root, show="*")
password.pack()

tk.Button(root, text="Login", width=15, bg="#1976d2", fg="white",
          command=login).pack(pady=20)

root.mainloop()
