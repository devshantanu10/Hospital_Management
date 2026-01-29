import tkinter as tk
from tkinter import ttk, messagebox


doctors = []

next_doctor_id = 1



d_name = d_age = d_gender = d_speciality = d_search = doctor_listbox = None

def build_doctor_ui(frame):
    global d_name, d_age, d_gender, d_speciality, d_search, doctor_listbox

    ttk.Label(frame, text="Name:").grid(row=0, column=0)
    d_name = ttk.Entry(frame)
    d_name.grid(row=0, column=1)

    ttk.Label(frame, text="Age:").grid(row=1, column=0)
    d_age = ttk.Entry(frame)
    d_age.grid(row=1, column=1)

    ttk.Label(frame, text="Gender:").grid(row=2, column=0)
    d_gender = ttk.Entry(frame)
    d_gender.grid(row=2, column=1)

    ttk.Label(frame, text="Speciality:").grid(row=3, column=0)
    d_speciality = ttk.Entry(frame)
    d_speciality.grid(row=3, column=1)

    ttk.Button(frame, text="Add Doctor", command=add_doctor).grid(row=4, column=0, columnspan=2)

    ttk.Label(frame, text="Search/ID:").grid(row=5, column=0)
    d_search = ttk.Entry(frame)
    d_search.grid(row=5, column=1)

    ttk.Button(frame, text="Find", command=find_doctor).grid(row=6, column=0)
    ttk.Button(frame, text="Delete", command=delete_doctor).grid(row=6, column=1)

    doctor_listbox = tk.Listbox(frame, width=60)
    doctor_listbox.grid(row=7, column=0, columnspan=2, pady=10)

def add_doctor():
    global next_doctor_id
    name = d_name.get()
    if not name:
        messagebox.showwarning("Oops", "Name is required")
        return

    doctors.append({
        "id": next_doctor_id,
        "name": name,
        "age": d_age.get(),
        "gender": d_gender.get(),
        "speciality": d_speciality.get()
    })
    next_doctor_id += 1
    d_name.delete(0, tk.END)
    d_age.delete(0,tk.END)
    d_gender.delete(0,tk.END)
    d_speciality.delete(0, tk.END)

    d_search.delete(0, tk.END)
    refresh_doctor_list()
    messagebox.showinfo("Success", "Doctors added")
    

def refresh_doctor_list():
    doctor_listbox.delete(0, tk.END)
    for d in doctors:
        doctor_listbox.insert(tk.END, f"ID {d['id']}: {d['name']} (Spec: {d['speciality']})")

def find_doctor():
    pid = d_search.get()
    if pid.isnumeric():
        pid = int(pid)
        for d in doctors:
            if d["id"] == pid:
                messagebox.showinfo("Found Doctor",
                    f"ID {d['id']}\nName: {d['name']}\nAge: {d['age']}\nGender: {d['gender']}\nSpec: {d['speciality']}")
                return
            
    
    messagebox.showerror("Error", "Doctor not found")

def delete_doctor():
    pid = d_search.get()
    if pid.isnumeric():
        pid = int(pid)
        for d in doctors:
            if d["id"] == pid:
                doctors.remove(d)
                refresh_doctor_list()
                messagebox.showinfo("Deleted", "Doctor removed")
                return
    messagebox.showerror("Error", "Doctor not found")