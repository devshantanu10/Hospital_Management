import tkinter as tk
from tkinter import ttk, messagebox



patients = []
next_patient_id = 1


d_name = d_age = d_gender = d_disease= d_search = doctor_listbox = None

def build_patient_ui(frame):
    global p_name, p_age, p_gender, p_disease, p_search, patient_listbox

    ttk.Label(frame, text="Name:").grid(row=0, column=0)
    p_name = ttk.Entry(frame)
    p_name.grid(row=0, column=1)

    ttk.Label(frame, text="Age:").grid(row=1, column=0)
    p_age = ttk.Entry(frame)
    p_age.grid(row=1, column=1)

    ttk.Label(frame, text="Gender:").grid(row=2, column=0)
    p_gender = ttk.Entry(frame)
    p_gender.grid(row=2, column=1)

    ttk.Label(frame, text="Disease:").grid(row=3, column=0)
    p_disease = ttk.Entry(frame)
    p_disease.grid(row=3, column=1)

    ttk.Button(frame, text="Add Patient", command=add_patient).grid(row=4, column=0, columnspan=2)

    ttk.Label(frame, text="Search/ID:").grid(row=5, column=0)
    p_search = ttk.Entry(frame)
    p_search.grid(row=5, column=1)

    ttk.Button(frame, text="Find", command=find_patient).grid(row=6, column=0)
    ttk.Button(frame, text="Delete", command=delete_patient).grid(row=6, column=1)

    patient_listbox = tk.Listbox(frame, width=60)
    patient_listbox.grid(row=7, column=0, columnspan=2, pady=10)

def add_patient():
    global next_patient_id
    name = p_name.get()
    if not name:
        messagebox.showwarning("Oops", "Name is required")
        return

    patients.append({
        "id": next_patient_id,
        "name": name,
        "age": p_age.get(),
        "gender": p_gender.get(),
        "disease": p_disease.get()
    })
    next_patient_id += 1
    p_name.delete(0, tk.END)
    p_age.delete(0, tk.END)
    p_gender.delete(0, tk.END)
    p_disease.delete(0, tk.END)

    # Clear the search box
    p_search.delete(0, tk.END)
    refresh_patient_list()
    messagebox.showinfo("Success" , "Patient Added")

def refresh_patient_list():
    patient_listbox.delete(0, tk.END)
    for p in patients:
        patient_listbox.insert(tk.END, f"ID {p['id']}: {p['name']} (Disease: {p['disease']})")

def find_patient():
    pid = p_search.get()
    if pid.isnumeric():
        pid = int(pid)
        for p in patients:
            if p["id"] == pid:
                messagebox.showinfo("Found Patient",
                    f"ID {p['id']}\nName: {p['name']}\nAge: {p['age']}\nGender: {p['gender']}\nDisease: {p['disease']}")
                return
    messagebox.showerror("Error", "Patient not found")

def delete_patient():
    pid = p_search.get()
    if pid.isnumeric():
        pid = int(pid)
        for p in patients:
            if p["id"] == pid:
                patients.remove(p)
                refresh_patient_list()
                messagebox.showinfo("Deleted", "Patient removed")