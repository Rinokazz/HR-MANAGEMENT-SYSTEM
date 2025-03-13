import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
import hashlib

# Hashing function for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# UI Styling Function
def style_ui(root):
    root.configure(bg='white')  # Set background color
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), relief=tk.RAISED, bd=5)
        elif isinstance(widget, tk.Label):
            widget.configure(bg='white', font=('Arial', 12))
        elif isinstance(widget, tk.Entry):
            widget.configure(bg='#f0f0f0', font=('Arial', 12))
        elif isinstance(widget, tk.Frame):
            widget.configure(bg='white')

# Login Window
def login():
    global username_entry, password_entry, login_window
    login_window = tk.Tk()
    login_window.title("HR Management System - Login")
    
    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=authenticate_user).pack()
    tk.Button(login_window, text="Forgot Password", command=forgot_password).pack()

    style_ui(login_window)
    login_window.mainloop()

# Authenticate User
def authenticate_user():
    username = username_entry.get()
    password = hash_password(password_entry.get())
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Arogundade",
            database="HR_Database"
        )
        cursor = conn.cursor()
        
        query = "SELECT Role FROM Users WHERE Username = %s AND PasswordHash = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        
        if result:
            role = result[0]
            messagebox.showinfo("Login Success", f"Welcome {username}! Role: {role}")
            login_window.destroy()
            open_dashboard(username, role)
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Forgot Password
def forgot_password():
    email = simpledialog.askstring("Forgot Password", "Enter your registered email:")
    if not email:
        return
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Arogundade",
            database="HR_Database"
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT Username FROM Users WHERE Email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            new_password = simpledialog.askstring("Reset Password", "Enter new password:", show="*")
            if new_password:
                hashed_password = hash_password(new_password)
                cursor.execute("UPDATE Users SET PasswordHash = %s WHERE Email = %s", (hashed_password, email))
                conn.commit()
                messagebox.showinfo("Success", "Password reset successfully!")
        else:
            messagebox.showerror("Error", "No user found with that email!")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Dashboard
def open_dashboard(username, role):
    dashboard = tk.Tk()
    dashboard.title("HR Management System")
    
    tk.Label(dashboard, text=f"Welcome {username} - Role: {role}", font=("Arial", 16)).pack()
    tk.Button(dashboard, text="Manage Employees", command=manage_employees).pack()
    tk.Button(dashboard, text="View Employees", command=view_employees).pack()
    tk.Button(dashboard, text="Logout", command=dashboard.destroy).pack()

    style_ui(dashboard)
    dashboard.mainloop()

# Manage Employees
def manage_employees():
    emp_window = tk.Toplevel()
    emp_window.title("Manage Employees")
    
    labels = ["First Name", "Last Name", "Phone Number", "Email", "Job ID", "Department ID", "Gender", "Salary", "Date of Birth", "Hire Date"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(emp_window, text=label + ":").grid(row=i, column=0)
        entry = tk.Entry(emp_window)
        entry.grid(row=i, column=1)
        entries[label] = entry
    
    def save_employee():
        values = {label: entry.get() for label, entry in entries.items()}
        if not values["First Name"] or not values["Last Name"]:
            messagebox.showerror("Error", "First Name and Last Name are required!")
            return
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Arogundade",
                database="HR_Database"
            )
            cursor = conn.cursor()
            
            query = """
            INSERT INTO Employees (FirstName, LastName, PhoneNumber, Email, JobID, DepartmentID, Gender, Salary, DateOfBirth, HireDate) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, tuple(values.values()))
            conn.commit()
            messagebox.showinfo("Success", "Employee added successfully!")
            
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
    
    tk.Button(emp_window, text="Save Employee", command=save_employee).grid(row=len(labels), column=0, columnspan=2)

    style_ui(emp_window)

# View Employees
def view_employees():
    emp_window = tk.Toplevel()
    emp_window.title("View Employees")
    
    columns = ("EmployeeID", "FirstName", "LastName", "PhoneNumber", "Email", "JobID", "DepartmentID", "Gender", "Salary", "DateOfBirth", "HireDate")
    tree = ttk.Treeview(emp_window, columns=columns, show="headings")
    tree.pack()
    
    for col in columns:
        tree.heading(col, text=col)
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Arogundade",
            database="HR_Database"
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Employees")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    style_ui(emp_window)

# Start Application
login()




cd "C:\Users\Sukanmi\Desktop\Data analysis\Database\hr_Database"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <https://github.com/Rinokazz/HR-MANAGEMENT-SYSTEM.git>
git push -u origin main
