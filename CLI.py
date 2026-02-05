import os

# ---------------- File Constants ----------------
PATIENT_FILE = "patients.txt"
DOCTOR_FILE = "doctors.txt"
ASSIGN_FILE = "assignments.txt"
DISCHARGED_FILE = "discharged.txt"

# ---------------- Login System ----------------
def login():

    VALID_USERS = {
        "admin": "1234",
        "doctor": "abcd"
    }

    attempts = 0
    while attempts < 3:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username in VALID_USERS and VALID_USERS[username] == password:
            print(f"Welcome, {username}!")
            return True
        else:
            attempts += 1
            print(f"Invalid credentials! Attempts left: {3 - attempts}")
    print("Too many failed attempts. Exiting…")
    return False

# ---------------- File Helpers ----------------
def read_file(file):
    if not os.path.exists(file):
        open(file, "w").close()
    with open(file) as f:
        return [line.strip() for line in f if line.strip()]

def write_file(file, lines):
    with open(file, "w") as f:
        for line in lines:
            f.write(line + "\n")

def generate_id(file):
    lines = read_file(file)
    if not lines:
        return 1
    return int(lines[-1].split("|")[0]) + 1

# ---------------- Patients ----------------
def list_patients():
    pats = read_file(PATIENT_FILE)
    if not pats:
        print("No patients found.")
        return
    print("ID | Name | Age | Gender")
    print("-" * 30)
    for p in pats:
        print(" | ".join(p.split("|")))

def add_patient():
    name = input("Enter patient name: ").strip()
    age = input("Enter age: ").strip()
    gender = input("Enter gender: ").strip()
    pid = generate_id(PATIENT_FILE)
    with open(PATIENT_FILE, "a") as f:
        f.write(f"{pid}|{name}|{age}|{gender}\n")
    print("Patient added.")

def update_patient():
    list_patients()
    pid = input("Enter patient ID: ").strip()
    pats = read_file(PATIENT_FILE)
    updated = []
    found = False
    for p in pats:
        parts = p.split("|")
        if parts[0] == pid:
            found = True
            print("Current:", p)
            new_name = input(f"New name ({parts[1]}): ").strip() or parts[1]
            new_age = input(f"New age ({parts[2]}): ").strip() or parts[2]
            new_gender = input(f"New gender ({parts[3]}): ").strip() or parts[3]
            updated.append(f"{pid}|{new_name}|{new_age}|{new_gender}")
        else:
            updated.append(p)
    if found:
        write_file(PATIENT_FILE, updated)
        print("Patient updated.")
    else:
        print("Patient not found.")

def remove_patient():
    list_patients()
    pid = input("Enter patient ID to remove: ").strip()
    pats = read_file(PATIENT_FILE)
    new = [p for p in pats if p.split("|")[0] != pid]
    write_file(PATIENT_FILE, new)

    pname = next((p.split("|")[1] for p in pats if p.split("|")[0] == pid), "")
    assigns = read_file(ASSIGN_FILE)
    assigns = [a for a in assigns if not a.startswith(f"{pname} ->")]
    write_file(ASSIGN_FILE, assigns)
    print("Patient removed.")

# ---------------- Doctors ----------------
def list_doctors():
    docs = read_file(DOCTOR_FILE)
    if not docs:
        print("No doctors found.")
        return
    print("ID | Name | Age | Gender")
    print("-" * 30)
    for d in docs:
        print(" | ".join(d.split("|")))

def add_doctor():
    name = input("Enter doctor name: ").strip()
    age = input("Enter age: ").strip()
    gender = input("Enter gender: ").strip()
    did = generate_id(DOCTOR_FILE)
    with open(DOCTOR_FILE, "a") as f:
        f.write(f"{did}|{name}|{age}|{gender}\n")
    print("Doctor added.")

def update_doctor():
    list_doctors()
    did = input("Enter doctor ID: ").strip()
    docs = read_file(DOCTOR_FILE)
    updated = []
    found = False
    for d in docs:
        parts = d.split("|")
        if parts[0] == did:
            found = True
            print("Current:", d)
            new_name = input(f"New name ({parts[1]}): ").strip() or parts[1]
            new_age = input(f"New age ({parts[2]}): ").strip() or parts[2]
            new_gender = input(f"New gender ({parts[3]}): ").strip() or parts[3]
            updated.append(f"{did}|{new_name}|{new_age}|{new_gender}")
        else:
            updated.append(d)
    if found:
        write_file(DOCTOR_FILE, updated)
        print("Doctor updated.")
    else:
        print("Doctor not found.")

def remove_doctor():
    list_doctors()
    did = input("Enter doctor ID to remove: ").strip()
    docs = read_file(DOCTOR_FILE)
    new = [d for d in docs if d.split("|")[0] != did]
    write_file(DOCTOR_FILE, new)

    dname = next((d.split("|")[1] for d in docs if d.split("|")[0] == did), "")
    assigns = read_file(ASSIGN_FILE)
    assigns = [a for a in assigns if not a.endswith(f" -> {dname}")]
    write_file(ASSIGN_FILE, assigns)
    print("Doctor removed.")

# ---------------- Assignments ----------------


def assign_doctor():
    # Show patients
    list_patients()
    pid = input("Enter patient ID: ").strip()

    # Look up patient name
    patient_list = read_file(PATIENT_FILE)
    pname = None
    for p in patient_list:
        parts = p.split("|")
        if parts[0] == pid:
            pname = parts[1]
            break
    if not pname:
        print("Invalid patient ID.")
        return

    # Show doctors
    list_doctors()
    did = input("Enter doctor ID: ").strip()

    # Look up doctor name
    doctor_list = read_file(DOCTOR_FILE)
    dname = None
    for d in doctor_list:
        parts = d.split("|")
        if parts[0] == did:
            dname = parts[1]
            break
    if not dname:
        print("Invalid doctor ID.")
        return

    # Create assignment with names
    
    assignment = f"{pname} -> {dname}"
    assigns = read_file(ASSIGN_FILE)
    if assignment in assigns:
        print("Already assigned.")
        return

    assigns.append(assignment)
    write_file(ASSIGN_FILE, assigns)

    print("Doctor assigned to patient.")
    print("Saved as:", assignment)


def view_assignments():
    assigns = read_file(ASSIGN_FILE)
    if not assigns:
        print("No assignments found.")
        return
    print("Patient -> Doctor")
    print("-"*30)
    for a in assigns:
        print(a)

# ---------------- Discharge ----------------
def discharge_patient():
    list_patients()
    pid = input("Enter patient ID to discharge: ").strip()
    pats = read_file(PATIENT_FILE)
    updated = []
    discharged_record = None
    for p in pats:
        if p.split("|")[0] == pid:
            discharged_record = p
        else:
            updated.append(p)
    if discharged_record:
        write_file(PATIENT_FILE, updated)
        with open(DISCHARGED_FILE, "a") as f:
            f.write(discharged_record + "\n")
        assigns = read_file(ASSIGN_FILE)
        assigns = [a for a in assigns if not a.startswith(discharged_record.split("|")[1])]
        write_file(ASSIGN_FILE, assigns)
        print("Patient discharged.")
    else:
        print("Patient not found.")

def list_discharged():
    dis = read_file(DISCHARGED_FILE)
    if not dis:
        print("No discharged patients.")
        return
    print("ID | Name | Age | Gender")
    print("-"*30)
    for p in dis:
        print(" | ".join(p.split("|")))

# ---------------- Menu ----------------
def menu():
    while True:
        print("""
1 List Patients
2 Add Patient
3 Update Patient
4 Remove Patient
5 List Doctors
6 Add Doctor
7 Update Doctor
8 Remove Doctor
9 Assign Doctor
10 View Assignments
11 Discharge Patient
12 List Discharged
0 Exit
        """)
        c = input("Enter choice: ").strip()
        match c:
            case "1": list_patients()
            case "2": add_patient()
            case "3": update_patient()
            case "4": remove_patient()
            case "5": list_doctors()
            case "6": add_doctor()
            case "7": update_doctor()
            case "8": remove_doctor()
            case "9": assign_doctor()
            case "10": view_assignments()
            case "11": discharge_patient()
            case "12": list_discharged()
            case "0":
                print("Goodbye!")
                return
            case _:
                print("Invalid choice.")

# ---------------- Run ----------------
if __name__ == "__main__":
    print("Hospital Management CLI")
    if login():
        menu()
