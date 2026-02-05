import tkinter as tk
from tkinter import messagebox, ttk

PATIENT_FILE = "patients.txt"
DOCTOR_FILE = "doctors.txt"
ASSIGN_FILE = "assignments.txt"

# ---------------- ID Generators ----------------
def generate_id(file):
    try:
        with open(file) as f:
            lines = f.readlines()
            if not lines:
                return 1
            last_id = int(lines[-1].split("|")[0])
            return last_id + 1
    except FileNotFoundError:
        return 1

# ---------------- CRUD ----------------
def save_patient():
    pid = generate_id(PATIENT_FILE)
    pname = name.get().strip()
    page = age.get().strip()
    pgender = gender.get().strip()
    if not pname or not page or not pgender:
        messagebox.showerror("Error", "All fields are required")
        return
    with open(PATIENT_FILE, "a") as f:
        f.write(f"{pid}|{pname}|{page}|{pgender}\n")
    name.delete(0, tk.END)
    age.delete(0, tk.END)
    gender.delete(0, tk.END)
    refresh()
    refresh_assignments()

def delete_patient():
    selected = listbox.curselection()
    if not selected:
        return
    patient_id_val = listbox.get(selected).split("|")[0]
    try:
        # Remove from patients.txt
        with open(PATIENT_FILE, "r") as f:
            patients = f.readlines()
        with open(PATIENT_FILE, "w") as f:
            for p in patients:
                if p.split("|")[0] != patient_id_val:
                    f.write(p)
        # Remove from assignments.txt
        assignments = read_file(ASSIGN_FILE)
        assignments = [a for a in assignments if not a.startswith(f"{patient_id_val} ->")]
        write_file(ASSIGN_FILE, assignments)
        refresh()
        refresh_assignments()
    except FileNotFoundError:
        pass

# ---------------- Assign Doctor ----------------
def assign_doctor():
    selected_patient = listbox.curselection()
    if not selected_patient:
        messagebox.showerror("Error", "Select a patient from the list")
        return
    patient_id_val = listbox.get(selected_patient).split("|")[0]
    doctor_selection = doctor_combo.get()
    if not doctor_selection:
        messagebox.showerror("Error", "Select a doctor")
        return
    doctor_id_val = doctor_selection.split("|")[0]

    # Check for duplicates
    existing = read_file(ASSIGN_FILE)
    if f"{patient_id_val} -> {doctor_id_val}" in existing:
        messagebox.showinfo("Info", "This doctor is already assigned to the patient")
        return

    # Save assignment
    with open(ASSIGN_FILE, "a") as f:
        f.write(f"{patient_id_val} -> {doctor_id_val}\n")
    messagebox.showinfo("Success", f"Doctor {doctor_selection.split('|')[1]} assigned to patient")
    doctor_combo.set("")
    refresh_assignments()

# ---------------- Helper Functions ----------------
def read_file(file):
    try:
        with open(file) as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []

def write_file(file, lines):
    with open(file, "w") as f:
        for line in lines:
            f.write(line + "\n")

# ---------------- Refresh ----------------
def refresh():
    listbox.delete(0, tk.END)
    patients = read_file(PATIENT_FILE)
    for p in patients:
        listbox.insert(tk.END, p)

def refresh_doctors():
    doctor_combo['values'] = read_file(DOCTOR_FILE)

def refresh_assignments():
    assignment_listbox.delete(0, tk.END)
    patients = {p.split("|")[0]: p.split("|")[1] for p in read_file(PATIENT_FILE)}
    doctors = {d.split("|")[0]: d.split("|")[1] for d in read_file(DOCTOR_FILE)}
    assignments = read_file(ASSIGN_FILE)
    for a in assignments:
        patient_id, doctor_id = a.split(" -> ")
        pname = patients.get(patient_id, "Unknown Patient")
        dname = doctors.get(doctor_id, "Unknown Doctor")
        assignment_listbox.insert(tk.END, f"{pname} -> {dname}")

# ---------------- View Assigned Doctors Button ----------------
def view_assignments_window():
    win = tk.Toplevel()
    win.title("Assigned Doctors")
    win.geometry("400x300")
    list_view = tk.Listbox(win, width=50)
    list_view.pack(pady=20)

    patients = {p.split("|")[0]: p.split("|")[1] for p in read_file(PATIENT_FILE)}
    doctors = {d.split("|")[0]: d.split("|")[1] for d in read_file(DOCTOR_FILE)}
    assignments = read_file(ASSIGN_FILE)

    if not assignments:
        list_view.insert(tk.END, "No assignments yet")
        return

    for a in assignments:
        patient_id, doctor_id = a.split(" -> ")
        pname = patients.get(patient_id, "Unknown Patient")
        dname = doctors.get(doctor_id, "Unknown Doctor")
        list_view.insert(tk.END, f"{pname} -> {dname}")

# ---------------- GUI ----------------
def open_patient_window():
    global name, age, gender, listbox, doctor_combo, assignment_listbox

    win = tk.Toplevel()
    win.title("Patients")
    win.geometry("700x500")

    tk.Label(win, text="Patient Name").pack()
    name = tk.Entry(win)
    name.pack()

    tk.Label(win, text="Age").pack()
    age = tk.Entry(win)
    age.pack()

    tk.Label(win, text="Gender").pack()
    gender = tk.Entry(win)
    gender.pack()

    tk.Button(win, text="Add Patient", command=save_patient).pack(pady=5)
    tk.Button(win, text="Delete Patient", command=delete_patient).pack(pady=5)

    tk.Label(win, text="Assign Doctor").pack(pady=5)
    doctor_combo = ttk.Combobox(win, width=50)
    doctor_combo.pack()
    tk.Button(win, text="Assign Selected Doctor", command=assign_doctor).pack(pady=5)

    tk.Button(win, text="View Assigned Doctors", command=view_assignments_window).pack(pady=10)

    tk.Label(win, text="Patients List").pack()
    listbox = tk.Listbox(win, width=70)
    listbox.pack(pady=5)

    tk.Label(win, text="Assigned Doctors (Quick View)").pack()
    assignment_listbox = tk.Listbox(win, width=70)
    assignment_listbox.pack(pady=5)

    # Initial refresh
    refresh()
    refresh_doctors()
    refresh_assignments()
