import tkinter as tk
from tkinter import messagebox

DOCTOR_FILE = "doctors.txt"

def generate_id():
    try:
        with open(DOCTOR_FILE) as f:
            lines = f.readlines()
            if not lines:
                return 1
            last_id = int(lines[-1].split("|")[0])
            return last_id + 1
    except FileNotFoundError:
        return 1

def save_doctor():
    did = generate_id()
    dname = name.get()
    dage = age.get()
    dgender = gender.get()
    if not dname or not dage or not dgender:
        messagebox.showerror("Error", "All fields are required")
        return
    with open(DOCTOR_FILE, "a") as f:
        f.write(f"{did}|{dname}|{dage}|{dgender}\n")
    refresh()
    name.delete(0, tk.END)
    age.delete(0, tk.END)
    gender.delete(0, tk.END)

def delete_doctor():
    selected = listbox.curselection()
    if not selected:
        return
    doctor = listbox.get(selected).split("|")[0]  # ID
    try:
        with open(DOCTOR_FILE, "r") as f:
            doctors = f.readlines()
        with open(DOCTOR_FILE, "w") as f:
            for d in doctors:
                if d.split("|")[0] != doctor:
                    f.write(d)
        refresh()
    except FileNotFoundError:
        pass

def refresh():
    listbox.delete(0, tk.END)
    try:
        with open(DOCTOR_FILE) as f:
            for d in f:
                listbox.insert(tk.END, d.strip())
    except FileNotFoundError:
        pass

def open_doctor_window():
    global name, age, gender, listbox

    win = tk.Toplevel()
    win.title("Doctors")
    win.geometry("500x400")

    tk.Label(win, text="Doctor Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Age").pack()
    age = tk.Entry(win)
    age.pack()

    tk.Label(win, text="Gender").pack()
    gender = tk.Entry(win)
    gender.pack()

    tk.Button(win, text="Add Doctor", command=save_doctor).pack(pady=5)
    tk.Button(win, text="Delete Doctor", command=delete_doctor).pack(pady=5)

    listbox = tk.Listbox(win, width=50)
    listbox.pack(pady=10)

    refresh()
