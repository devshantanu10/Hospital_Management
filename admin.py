import tkinter as tk
import patients
import doctors

def open_admin():
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("500x400")
    root.configure(bg="#f1f8e9")

    tk.Label(root, text="Hospital Management System",
             font=("Arial", 18, "bold"), bg="#f1f8e9").pack(pady=20)

    tk.Button(root, text="Manage Patients", width=25, height=2,
              command=patients.open_patient_window).pack(pady=10)

    tk.Button(root, text="Manage Doctors", width=25, height=2,
              command=doctors.open_doctor_window).pack(pady=10)

    tk.Button(root, text="Exit", width=25, height=2,
              bg="#d32f2f", fg="white",
              command=root.destroy).pack(pady=20)

    root.mainloop()
