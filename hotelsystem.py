"""
Hotel management starter script.

Behavior:
- On run, a small Tkinter window appears asking for the MySQL password.
- The password is validated by attempting a connection to the MySQL server.
- If valid, the script creates the `hotel_db` database and required tables (if they don't exist),
  inserts sample data, and then opens the user login GUI (username/password stored in `users` table).
- CRUD functions are available in the module and use the validated password for connections.

"""
import os
import sys
from getpass import getpass
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# ---------------------------
# Configuration and globals
# ---------------------------
DB_PASSWORD = os.getenv("DB_PASS") or None
DB_HOST = "localhost"
DB_USER = "root"
DB_NAME = "hotel_db"

# ---------------------------
# Helper: DB connection
# ---------------------------
def get_connection(database: str = DB_NAME):
    """Return a mysql.connector connection using the validated global DB_PASSWORD."""
    global DB_PASSWORD
    if not DB_PASSWORD:
        raise RuntimeError("Database password not set. Authenticate first.")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=database
        )
        return conn
    except Error as e:
        raise

# ---------------------------
# Database creation / setup
# ---------------------------
def create_database_and_tables(password: str):
    """Create database and tables and insert sample data using the provided password."""
    try:
        # Connect to server (no database specified)
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cursor.execute(f"USE `{DB_NAME}`")

        tables = [
            """CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE,
                password VARCHAR(255)
            )""",
            """CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                phone VARCHAR(20),
                email VARCHAR(100),
                address VARCHAR(200)
            )""",
            """CREATE TABLE IF NOT EXISTS rooms (
                id INT AUTO_INCREMENT PRIMARY KEY,
                room_number INT UNIQUE,
                room_type VARCHAR(50),
                price DECIMAL(10,2),
                status VARCHAR(20) DEFAULT 'Available'
            )""",
            """CREATE TABLE IF NOT EXISTS bookings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                room_id INT,
                check_in DATE,
                check_out DATE,
                total_amount DECIMAL(10,2),
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )"""
        ]

        for sql in tables:
            cursor.execute(sql)

        # Insert sample data (use INSERT IGNORE semantics)
        # MySQL's INSERT IGNORE works with unique constraints; use parameterized query for safety.
        cursor.execute("INSERT IGNORE INTO users (username, password) VALUES (%s, %s)", ("admin", "admin123"))

        room_data = [
            (101, 'Single', 50.00),
            (102, 'Double', 80.00),
            (103, 'Suite', 150.00)
        ]
        query = "INSERT IGNORE INTO rooms (room_number, room_type, price) VALUES (%s, %s, %s)"
        cursor.executemany(query, room_data)

        conn.commit()
        cursor.close()
        conn.close()
        print("Database and tables created (or already existed). Sample data inserted.")
    except Error as e:
        print(f"Error while creating database/tables: {e}")
        sys.exit(1)

# ---------------------------
# CRUD functions (users)
# ---------------------------
def create_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    cursor.close()
    conn.close()

def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_user(user_id, new_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_password, user_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# CRUD functions (customers)
# ---------------------------
def create_customer(name, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone, email, address) VALUES (%s, %s, %s, %s)",
                   (name, phone, email, address))
    conn.commit()
    cursor.close()
    conn.close()

def get_customers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_customer(customer_id, phone, email, address):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET phone=%s, email=%s, address=%s WHERE id=%s",
                   (phone, email, address, customer_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id=%s", (customer_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# CRUD functions (rooms)
# ---------------------------
def create_room(room_number, room_type, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rooms (room_number, room_type, price) VALUES (%s, %s, %s)",
                   (room_number, room_type, price))
    conn.commit()
    cursor.close()
    conn.close()

def get_rooms():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_room_status(room_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE rooms SET status=%s WHERE id=%s", (status, room_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_room(room_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rooms WHERE id=%s", (room_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# CRUD functions (bookings)
# ---------------------------
def create_booking(customer_id, room_id, check_in, check_out, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO bookings (customer_id, room_id, check_in, check_out, total_amount)
                      VALUES (%s, %s, %s, %s, %s)""",
                   (customer_id, room_id, check_in, check_out, total_amount))
    conn.commit()
    cursor.close()
    conn.close()

def get_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""SELECT b.id, c.name, r.room_number, b.check_in, b.check_out, b.total_amount
                      FROM bookings b
                      JOIN customers c ON b.customer_id = c.id
                      JOIN rooms r ON b.room_id = r.id""")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def update_booking(booking_id, check_out, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET check_out=%s, total_amount=%s WHERE id=%s",
                   (check_out, total_amount, booking_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_booking(booking_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# GUI: Password prompt (first thing shown)
# ---------------------------
class PasswordPrompt:
    """
    Small modal window that asks for the MySQL password on startup.
    Validates the password by attempting to connect to the MySQL server.
    On success, sets the global DB_PASSWORD and closes.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Enter MySQL Password")
        self.root.geometry("360x140")
        self.root.resizable(False, False)

        self.pass_var = tk.StringVar()

        tk.Label(root, text="Enter MySQL password for user 'root':").pack(pady=(12, 6))
        self.entry = tk.Entry(root, textvariable=self.pass_var, show="*", width=36)
        self.entry.pack(pady=6)
        self.entry.focus_set()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Submit", width=10, command=self.on_submit).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Cancel", width=10, command=self.on_cancel).pack(side="left", padx=6)

        # Allow Enter key to submit
        root.bind("<Return>", lambda event: self.on_submit())

    def on_submit(self):
        global DB_PASSWORD
        pwd = self.pass_var.get().strip() or None

        if not pwd:
            # fallback to console prompt if GUI password empty and env not set
            try:
                pwd = getpass("Enter MySQL Password: ")
            except Exception:
                pwd = None

        if not pwd:
            messagebox.showerror("Error", "No password provided.")
            return

        # Validate credentials by attempting a connection to the server
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=pwd
            )
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Connection Error", f"Could not connect to MySQL server: {e}")
            self.pass_var.set("")
            self.entry.focus_set()
            return

        if row:
            DB_PASSWORD = pwd
            messagebox.showinfo("Success", "Password validated.")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")
            self.pass_var.set("")
            self.entry.focus_set()

    def on_cancel(self):
        self.root.destroy()

# ---------------------------
# GUI: Login window (after DB password validated and DB created)
# ---------------------------
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel System Login")
        self.root.geometry("420x260")
        self.root.resizable(False, False)
        self.user_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        # Styling (simple)
        bg = "#2c3e50"
        fg = "#ecf0f1"
        entry_bg = "#ecf0f1"
        entry_fg = "#2c3e50"

        self.root.configure(bg=bg)
        tk.Label(root, text="Login System", font=("Arial", 18, "bold"),
                 bg=bg, fg=fg).pack(pady=18)

        tk.Label(root, text="Username:", bg=bg, fg=fg).pack()
        self.username_entry = tk.Entry(root, textvariable=self.user_var, bg=entry_bg, fg=entry_fg)
        self.username_entry.pack(pady=6)

        tk.Label(root, text="Password:", bg=bg, fg=fg).pack()
        self.password_entry = tk.Entry(root, textvariable=self.pass_var, show="*", bg=entry_bg, fg=entry_fg)
        self.password_entry.pack(pady=6)

        tk.Button(root, text="Login", command=self.login_action, width=16,
                  bg="#27ae60", fg="white", activebackground="#2ecc71").pack(pady=14)

    def login_action(self):
        user = self.user_var.get().strip()
        pwd = self.pass_var.get().strip()

        if not user or not pwd:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        try:
            conn = get_connection()
        except Exception as e:
            messagebox.showerror("Error", f"Database connection failed: {e}")
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pwd))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
        except Error as e:
            messagebox.showerror("Error", f"Query failed: {e}")
            return

        if row:
            messagebox.showinfo("Success", f"Welcome, {user}!")
            # Here you could open the main application window / dashboard
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
            self.pass_var.set("")
            self.password_entry.focus_set()

# ---------------------------
# Main entrypoint
# ---------------------------
def main():
    global DB_PASSWORD

    # 1) Show password prompt GUI first
    pw_root = tk.Tk()
    pw_app = PasswordPrompt(pw_root)
    pw_root.mainloop()

    # If user closed the prompt without providing a valid password, exit
    if not DB_PASSWORD:
        print("No valid database password provided. Exiting.")
        sys.exit(1)

    # 2) Create DB and tables (if not present)
    create_database_and_tables(DB_PASSWORD)

    # 3) Launch login GUI (application-level login)
    login_root = tk.Tk()
    login_app = LoginApp(login_root)
    login_root.mainloop()

if __name__ == "__main__":
    main()

                                     
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

# Import your CRUD functions here
from crud_functions import (
    create_user, get_users, update_user, delete_user,
    create_customer, get_customers, update_customer, delete_customer,
    create_room, get_rooms, update_room_status, delete_room,
    create_booking, get_bookings, update_booking, delete_booking,
)

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Hotel Management System")
root.geometry("700x480")
root.configure(bg="#0f1724")  # deep navy background

style = ttk.Style()
style.theme_use("clam")

# ---------- Global font and spacing ----------
BASE_FONT = ("Segoe UI", 10)
HEADER_FONT = ("Segoe UI", 14, "bold")
BTN_FONT = ("Segoe UI", 11, "bold")

# ---------- Button styles ----------
style.configure("Primary.TButton",
                font=BTN_FONT,
                foreground="#ffffff",
                background="#0b84ff",
                padding=8,
                borderwidth=0)
style.map("Primary.TButton",
          background=[("active", "#0666d6")])

style.configure("Accent.TButton",
                font=BTN_FONT,
                foreground="#ffffff",
                background="#ff7a59",
                padding=8,
                borderwidth=0)
style.map("Accent.TButton",
          background=[("active", "#e05f3f")])

style.configure("Danger.TButton",
                font=BTN_FONT,
                foreground="#ffffff",
                background="#ff4d6d",
                padding=8,
                borderwidth=0)
style.map("Danger.TButton",
          background=[("active", "#e03a56")])

# ---------- Label and entry styles ----------
style.configure("TLabel",
                font=BASE_FONT,
                foreground="#e6eef8",
                background="#0f1724")
style.configure("Card.TFrame",
                background="#0b1220",
                borderwidth=0)
style.configure("TEntry",
                fieldbackground="#ffffff",
                background="#ffffff",
                foreground="#0b1220",
                padding=6)

# ---------- Treeview styles ----------
style.configure("Treeview",
                background="#f7fafc",
                foreground="#0b1220",
                fieldbackground="#f7fafc",
                rowheight=24,
                font=BASE_FONT)
style.configure("Treeview.Heading",
                font=("Segoe UI", 10, "bold"),
                background="#0b84ff",
                foreground="#ffffff")
style.map("Treeview.Heading",
          background=[("active", "#0666d6")])

# ---------- Header ----------
header_frame = ttk.Frame(root, style="Card.TFrame", padding=(12, 12, 12, 12))
header_frame.pack(fill="x", padx=16, pady=(16, 8))

header_label = ttk.Label(header_frame, text="Hotel Management System", font=HEADER_FONT, foreground="#ffffff", background="#0b1220")
header_label.pack(side="left")

sub_label = ttk.Label(header_frame, text="Manage users, customers, rooms and bookings", font=BASE_FONT, foreground="#cfe8ff", background="#0b1220")
sub_label.pack(side="left", padx=(12, 0))

# ---------- Main menu container ----------
menu_frame = ttk.Frame(root, style="Card.TFrame", padding=(16, 16, 16, 16))
menu_frame.pack(fill="both", expand=True, padx=16, pady=12)

# Helper to create labeled entry rows inside a frame
def labeled_entry(parent, label_text):
    lbl = ttk.Label(parent, text=label_text)
    ent = ttk.Entry(parent)
    return lbl, ent

# ---------------- USERS FRAME ----------------
def users_frame():
    frame = tk.Toplevel(root)
    frame.title("Manage Users")
    frame.geometry("520x340")
    frame.configure(bg="#e8f4ff")  # pale blue

    container = ttk.Frame(frame, padding=12)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    ttk.Label(container, text="Create New User", font=("Segoe UI", 12, "bold"), foreground="#0b3a66").pack(anchor="w", pady=(0,8))

    lbl_user, entry_username = labeled_entry(container, "Username")
    lbl_user.pack(anchor="w")
    entry_username.pack(fill="x", pady=(0,8))

    lbl_pass, entry_password = labeled_entry(container, "Password")
    lbl_pass.pack(anchor="w")
    entry_password = ttk.Entry(container, show="*")
    entry_password.pack(fill="x", pady=(0,8))

    def add_user():
        username = entry_username.get()
        password = entry_password.get()
        create_user(username, password)
        messagebox.showinfo("Success", "User created successfully!")

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill="x", pady=(10,0))
    ttk.Button(btn_frame, text="Add User", style="Primary.TButton", command=add_user).pack(side="left", padx=(0,8))
    ttk.Button(btn_frame, text="View Users", style="Accent.TButton", command=lambda: show_data(get_users())).pack(side="left")

# ---------------- CUSTOMERS FRAME ----------------
def customers_frame():
    frame = tk.Toplevel(root)
    frame.title("Manage Customers")
    frame.geometry("520x420")
    frame.configure(bg="#fff6f8")  # pale pink

    container = ttk.Frame(frame, padding=12)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    ttk.Label(container, text="Add Customer", font=("Segoe UI", 12, "bold"), foreground="#6b1f3a").pack(anchor="w", pady=(0,8))

    ttk.Label(container, text="Name").pack(anchor="w")
    entry_name = ttk.Entry(container)
    entry_name.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Phone").pack(anchor="w")
    entry_phone = ttk.Entry(container)
    entry_phone.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Email").pack(anchor="w")
    entry_email = ttk.Entry(container)
    entry_email.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Address").pack(anchor="w")
    entry_address = ttk.Entry(container)
    entry_address.pack(fill="x", pady=(0,6))

    def add_customer():
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        create_customer(name, phone, email, address)
        messagebox.showinfo("Success", "Customer created successfully!")

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill="x", pady=(10,0))
    ttk.Button(btn_frame, text="Add Customer", style="Primary.TButton", command=add_customer).pack(side="left", padx=(0,8))
    ttk.Button(btn_frame, text="View Customers", style="Accent.TButton", command=lambda: show_data(get_customers())).pack(side="left")

# ---------------- ROOMS FRAME ----------------
def rooms_frame():
    frame = tk.Toplevel(root)
    frame.title("Manage Rooms")
    frame.geometry("520x360")
    frame.configure(bg="#f0fff6")  # pale mint

    container = ttk.Frame(frame, padding=12)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    ttk.Label(container, text="Add Room", font=("Segoe UI", 12, "bold"), foreground="#0b5f3a").pack(anchor="w", pady=(0,8))

    ttk.Label(container, text="Room Number").pack(anchor="w")
    entry_room_number = ttk.Entry(container)
    entry_room_number.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Room Type").pack(anchor="w")
    entry_room_type = ttk.Entry(container)
    entry_room_type.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Price").pack(anchor="w")
    entry_price = ttk.Entry(container)
    entry_price.pack(fill="x", pady=(0,6))

    def add_room():
        try:
            room_number = int(entry_room_number.get())
            room_type = entry_room_type.get()
            price = float(entry_price.get())
            create_room(room_number, room_type, price)
            messagebox.showinfo("Success", "Room created successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for room number and price.")

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill="x", pady=(10,0))
    ttk.Button(btn_frame, text="Add Room", style="Primary.TButton", command=add_room).pack(side="left", padx=(0,8))
    ttk.Button(btn_frame, text="View Rooms", style="Accent.TButton", command=lambda: show_data(get_rooms())).pack(side="left")

# ---------------- BOOKINGS FRAME ----------------
def bookings_frame():
    frame = tk.Toplevel(root)
    frame.title("Manage Bookings")
    frame.geometry("520x420")
    frame.configure(bg="#fffde6")  # pale yellow

    container = ttk.Frame(frame, padding=12)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    ttk.Label(container, text="Create Booking", font=("Segoe UI", 12, "bold"), foreground="#6b4b00").pack(anchor="w", pady=(0,8))

    ttk.Label(container, text="Customer ID").pack(anchor="w")
    entry_customer_id = ttk.Entry(container)
    entry_customer_id.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Room ID").pack(anchor="w")
    entry_room_id = ttk.Entry(container)
    entry_room_id.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Check-in (YYYY-MM-DD)").pack(anchor="w")
    entry_check_in = ttk.Entry(container)
    entry_check_in.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Check-out (YYYY-MM-DD)").pack(anchor="w")
    entry_check_out = ttk.Entry(container)
    entry_check_out.pack(fill="x", pady=(0,6))

    ttk.Label(container, text="Total Amount").pack(anchor="w")
    entry_total = ttk.Entry(container)
    entry_total.pack(fill="x", pady=(0,6))

    def add_booking():
        try:
            customer_id = int(entry_customer_id.get())
            room_id = int(entry_room_id.get())
            check_in = entry_check_in.get()
            check_out = entry_check_out.get()
            total_amount = float(entry_total.get())
            create_booking(customer_id, room_id, check_in, check_out, total_amount)
            messagebox.showinfo("Success", "Booking created successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for IDs and total amount.")

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill="x", pady=(10,0))
    ttk.Button(btn_frame, text="Add Booking", style="Primary.TButton", command=add_booking).pack(side="left", padx=(0,8))
    ttk.Button(btn_frame, text="View Bookings", style="Accent.TButton", command=lambda: show_data(get_bookings())).pack(side="left")

# ---------------- DATA DISPLAY ----------------
def show_data(data):
    display = tk.Toplevel(root)
    display.title("Data Viewer")
    display.geometry("760x480")
    display.configure(bg="#0f1724")

    container = ttk.Frame(display, padding=12)
    container.pack(fill="both", expand=True, padx=12, pady=12)

    tree = ttk.Treeview(container)
    tree.pack(fill="both", expand=True)

    # Add a scrollbar
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    if data:
        # Ensure data is list of dicts
        tree["columns"] = list(data[0].keys())
        tree["show"] = "headings"
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
        for row in data:
            tree.insert("", "end", values=list(row.values()))
    else:
        ttk.Label(container, text="No data to display", font=BASE_FONT, foreground="#cfe8ff").pack(pady=20)

# ---------------- MAIN MENU BUTTONS ----------------
buttons = [
    ("Manage Users", users_frame, "Primary.TButton"),
    ("Manage Customers", customers_frame, "Accent.TButton"),
    ("Manage Rooms", rooms_frame, "Primary.TButton"),
    ("Manage Bookings", bookings_frame, "Accent.TButton"),
]

for text, cmd, style_name in buttons:
    btn = ttk.Button(menu_frame, text=text, command=cmd, style=style_name)
    btn.pack(fill="x", pady=8)

# Footer
footer = ttk.Label(root, text=f"Today: {date.today().isoformat()}", font=("Segoe UI", 9), foreground="#9fb7d9", background="#0f1724")
footer.pack(side="bottom", pady=(0,12))

root.mainloop()
