import tkinter as tk
from tkinter import ttk, messagebox

from patients import build_patient_ui, patients, refresh_patient_list
from doctors import build_doctor_ui, doctors, refresh_doctor_list

VALID_USERNAME = "admin"
VALID_PASSWORD = "swosti"

def attempt_login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        show_main_ui()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

def show_main_ui():
    for widget in root.winfo_children():
        widget.destroy()


    root.title("Hospital Management System")
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    patient_frame = ttk.Frame(notebook)
    doctor_frame = ttk.Frame(notebook)

    notebook.add(patient_frame, text="Patients")
    notebook.add(doctor_frame, text="Doctors")

    build_patient_ui(patient_frame)
    build_doctor_ui(doctor_frame)

root = tk.Tk()
root.title("Login")

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Button(root, text="Login", command=attempt_login).pack(pady=10)

root.mainloop()
