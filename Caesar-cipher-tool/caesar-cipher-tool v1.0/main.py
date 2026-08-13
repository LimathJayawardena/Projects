import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

# --- CONFIGURATION ---
# The "Main Mail" - This user will ALWAYS be an Admin.
SUPER_ADMIN_EMAIL = "admin@gmail.com"

# ==========================================
# PART 1: DATABASE MANAGER
# ==========================================


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("app_data.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Create a table for Users
        # Columns: id, email, password, role, score, is_online
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT DEFAULT 'Visitor',
                score INTEGER DEFAULT 0,
                is_online INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    def add_user(self, email, password):
        try:
            # If it's the super admin email, give them Admin role immediately
            role = 'Admin' if email == SUPER_ADMIN_EMAIL else 'Visitor'
            self.cursor.execute('INSERT INTO users (email, password, role) VALUES (?, ?, ?)',
                                (email, password, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Email already exists

    def check_login(self, email, password):
        self.cursor.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = self.cursor.fetchone()
        return user  # Returns the user row or None

    def set_online_status(self, email, status):
        # 1 for Online (Green), 0 for Offline (Red)
        self.cursor.execute(
            'UPDATE users SET is_online = ? WHERE email = ?', (status, email))
        self.conn.commit()

    def update_score(self, email, new_score):
        self.cursor.execute(
            'UPDATE users SET score = ? WHERE email = ?', (new_score, email))
        self.conn.commit()

    def reset_password(self, email, new_pass):
        self.cursor.execute(
            'UPDATE users SET password = ? WHERE email = ?', (new_pass, email))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_all_users(self):
        self.cursor.execute('SELECT email, role, score, is_online FROM users')
        return self.cursor.fetchall()

    def toggle_role(self, email):
        # Switch between Visitor and Admin
        self.cursor.execute('SELECT role FROM users WHERE email = ?', (email,))
        current_role = self.cursor.fetchone()[0]

        if email == SUPER_ADMIN_EMAIL:
            return False  # Cannot change Super Admin

        new_role = 'Admin' if current_role == 'Visitor' else 'Visitor'
        self.cursor.execute(
            'UPDATE users SET role = ? WHERE email = ?', (new_role, email))
        self.conn.commit()
        return new_role

# ==========================================
# PART 2: THE MAIN APPLICATION CLASS
# ==========================================


class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Cipher System")
        self.root.geometry("600x750")
        self.root.configure(bg="#f0f2f5")

        self.db = Database()
        self.current_user_email = None
        self.current_user_role = None
        self.current_user_score = 0

        # Container for all frames (pages)
        self.container = tk.Frame(root, bg="#f0f2f5")
        self.container.pack(fill="both", expand=True)

        # Dictionary to store frames
        self.frames = {}

        # Create all pages
        for F in (LoginPage, SignupPage, ForgotPassPage, MainPage, AdminPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()  # Bring frame to top

        # Refresh data if opening Admin or Main page
        if page_name == "AdminPage":
            frame.load_data()
        if page_name == "MainPage":
            frame.update_ui()

    def login_success(self, email, role, score):
        self.current_user_email = email
        self.current_user_role = role
        self.current_user_score = score
        self.db.set_online_status(email, 1)  # Set Green Dot
        self.show_frame("MainPage")

    def logout(self):
        if self.current_user_email:
            self.db.set_online_status(
                self.current_user_email, 0)  # Set Red Dot
        self.current_user_email = None
        self.show_frame("LoginPage")

# ==========================================
# PAGE 1: LOGIN
# ==========================================


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")
        self.controller = controller

        # UI Elements
        tk.Label(self, text="CYBER SECURITY SYSTEM", font=(
            "Helvetica", 18, "bold"), fg="blue", bg="white").pack(pady=(50, 10))
        tk.Label(self, text="USER LOGIN", font=("Arial", 14),
                 bg="white", fg="#555").pack(pady=10)

        tk.Label(self, text="Email Address:", bg="white",
                 font=("Arial", 10, "bold")).pack(pady=5)
        self.entry_email = tk.Entry(
            self, width=30, font=("Arial", 12), bg="#f8f9fa")
        self.entry_email.pack(pady=5)

        tk.Label(self, text="Password:", bg="white",
                 font=("Arial", 10, "bold")).pack(pady=5)
        self.entry_pass = tk.Entry(
            self, width=30, show="*", font=("Arial", 12), bg="#f8f9fa")
        self.entry_pass.pack(pady=5)

        tk.Button(self, text="LOGIN NOW", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=25, height=2,
                  command=self.do_login).pack(pady=20)

        # Footer Links
        tk.Label(self, text="---------------- OR ----------------",
                 bg="white", fg="#aaa").pack(pady=5)

        tk.Button(self, text="Create New Account", bg="white", fg="blue", font=("Arial", 10, "underline"), borderwidth=0,
                  command=lambda: controller.show_frame("SignupPage")).pack(pady=2)

        tk.Button(self, text="Forgot Password?", bg="white", fg="red", font=("Arial", 9), borderwidth=0,
                  command=lambda: controller.show_frame("ForgotPassPage")).pack(pady=2)

    def do_login(self):
        email = self.entry_email.get()
        pwd = self.entry_pass.get()

        user = self.controller.db.check_login(email, pwd)

        if user:
            # user row: (id, email, password, role, score, is_online)
            self.controller.login_success(user[1], user[3], user[4])
            # Clear boxes
            self.entry_email.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Login Failed", "Invalid Email or Password.\nTry again or Create an Account.")

# ==========================================
# PAGE 2: SIGNUP
# ==========================================


class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="CREATE ACCOUNT", font=("Helvetica", 18,
                 "bold"), bg="white", fg="#2196F3").pack(pady=50)

        tk.Label(self, text="Enter Email:", bg="white").pack()
        self.entry_email = tk.Entry(self, width=30, font=("Arial", 11))
        self.entry_email.pack(pady=5)

        tk.Label(self, text="Create Password:", bg="white").pack()
        self.entry_pass = tk.Entry(self, width=30, font=("Arial", 11))
        self.entry_pass.pack(pady=5)

        tk.Button(self, text="SIGN UP", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), width=20,
                  command=self.do_signup).pack(pady=20)

        tk.Button(self, text="< Back to Login", bg="white",
                  command=lambda: controller.show_frame("LoginPage")).pack()

    def do_signup(self):
        email = self.entry_email.get()
        pwd = self.entry_pass.get()

        if not email or not pwd:
            messagebox.showerror("Error", "All fields required")
            return

        success = self.controller.db.add_user(email, pwd)
        if success:
            messagebox.showinfo(
                "Success", "Account created successfully!\nYou can now Login.")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "This Email is already registered!")

# ==========================================
# PAGE 3: FORGOT PASSWORD
# ==========================================


class ForgotPassPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")
        self.controller = controller

        tk.Label(self, text="RESET PASSWORD", font=(
            "Helvetica", 18, "bold"), bg="white", fg="orange").pack(pady=50)

        tk.Label(self, text="Your Email:", bg="white").pack()
        self.entry_email = tk.Entry(self, width=30)
        self.entry_email.pack(pady=5)

        tk.Label(self, text="New Password:", bg="white").pack()
        self.entry_pass = tk.Entry(self, width=30)
        self.entry_pass.pack(pady=5)

        tk.Button(self, text="UPDATE PASSWORD", bg="#FF9800", fg="white", font=("Arial", 11, "bold"), width=20,
                  command=self.do_reset).pack(pady=20)

        tk.Button(self, text="< Back to Login", bg="white",
                  command=lambda: controller.show_frame("LoginPage")).pack()

    def do_reset(self):
        email = self.entry_email.get()
        pwd = self.entry_pass.get()
        if self.controller.db.reset_password(email, pwd):
            messagebox.showinfo("Success", "Password updated successfully.")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "Email not found in database.")

# ==========================================
# PAGE 4: MAIN APP (Cipher & Quiz)
# ==========================================


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#f0f2f5")
        self.controller = controller
        self.secret_key = 0

        # Header Info
        header_frame = tk.Frame(self, bg="#333", pady=10)
        header_frame.pack(fill="x")

        self.lbl_welcome = tk.Label(header_frame, text="Welcome", font=(
            "Arial", 12, "bold"), bg="#333", fg="white")
        self.lbl_welcome.pack(side="left", padx=20)

        tk.Button(header_frame, text="LOGOUT", bg="#d9534f", fg="white", font=("Arial", 8, "bold"),
                  command=controller.logout).pack(side="right", padx=20)

        # Admin Button (Hidden by default)
        self.btn_admin = tk.Button(self, text="🔒 OPEN ADMIN DB", bg="#d9534f", fg="white", font=("Arial", 12, "bold"),
                                   command=lambda: controller.show_frame("AdminPage"))

        # --- CIPHER TOOL SECTION ---
        frame_tool = tk.LabelFrame(self, text=" Encryption Tool ", bg="white", font=(
            "Arial", 11, "bold"), padx=15, pady=15)
        frame_tool.pack(padx=20, pady=15, fill="x")

        tk.Label(frame_tool, text="Type your Message:",
                 bg="white", fg="#666").pack(anchor="w")
        self.entry_msg = tk.Entry(frame_tool, font=("Arial", 11), width=40)
        self.entry_msg.pack(fill="x", pady=(0, 10))

        tk.Label(frame_tool, text="Shift Key (Number):",
                 bg="white", fg="#666").pack(anchor="w")
        self.entry_shift = tk.Entry(frame_tool, font=("Arial", 11), width=10)
        self.entry_shift.insert(0, "3")
        self.entry_shift.pack(anchor="w", pady=(0, 10))

        btn_frame = tk.Frame(frame_tool, bg="white")
        btn_frame.pack(pady=5, fill="x")
        tk.Button(btn_frame, text="ENCRYPT", bg="#4CAF50", fg="white",
                  width=15, command=self.encrypt).pack(side="left", padx=5)
        tk.Button(btn_frame, text="DECRYPT", bg="#2196F3", fg="white",
                  width=15, command=self.decrypt).pack(side="right", padx=5)

        tk.Label(frame_tool, text="Result:", bg="white", font=(
            "Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.entry_res = tk.Entry(
            frame_tool, font=("Consolas", 11), bg="#f8f9fa")
        self.entry_res.pack(fill="x", pady=5)

        # --- QUIZ SECTION ---
        frame_quiz = tk.LabelFrame(self, text=" Quiz Challenge ", bg="white", font=(
            "Arial", 11, "bold"), padx=15, pady=15)
        frame_quiz.pack(padx=20, pady=10, fill="x")

        self.lbl_score = tk.Label(frame_quiz, text="Your Score: 0", font=(
            "Arial", 12, "bold"), fg="#673AB7", bg="white")
        self.lbl_score.pack(anchor="e")

        tk.Button(frame_quiz, text="Generate New Challenge", bg="#FF9800",
                  fg="white", command=self.new_quiz).pack(fill="x", pady=5)

        tk.Label(frame_quiz, text="Decrypt this message:",
                 bg="white", fg="#666").pack(anchor="w")
        self.lbl_challenge = tk.Label(frame_quiz, text="[Press Generate]", font=(
            "Consolas", 12, "bold"), bg="#f0f0f0", width=30, height=2, relief="sunken")
        self.lbl_challenge.pack(pady=5, fill="x")

        tk.Label(frame_quiz, text="What was the shift key?",
                 bg="white").pack(anchor="w")
        self.entry_guess = tk.Entry(frame_quiz, width=10)
        self.entry_guess.pack(anchor="w")

        tk.Button(frame_quiz, text="Submit Answer", bg="#673AB7",
                  fg="white", command=self.check_answer).pack(pady=10)

    def update_ui(self):
        email = self.controller.current_user_email
        role = self.controller.current_user_role
        score = self.controller.current_user_score

        self.lbl_welcome.config(text=f"User: {email} | Role: {role}")
        self.lbl_score.config(text=f"Your Score: {score}")

        # Show Admin Button ONLY if role is Admin
        if role == 'Admin':
            self.btn_admin.pack(after=self.lbl_welcome.master, pady=10)
        else:
            self.btn_admin.pack_forget()

    # Logic Functions
    def encrypt(self): self.run_cipher('encrypt')
    def decrypt(self): self.run_cipher('decrypt')

    def run_cipher(self, mode):
        txt = self.entry_msg.get()
        try:
            s = int(self.entry_shift.get())
            if mode == 'decrypt':
                s = -s
            res = ""
            for c in txt:
                if c.isalpha():
                    start = ord('A') if c.isupper() else ord('a')
                    res += chr((ord(c) - start + s) % 26 + start)
                else:
                    res += c
            self.entry_res.delete(0, tk.END)
            self.entry_res.insert(0, res)
        except:
            messagebox.showerror("Error", "Shift must be a valid number")

    def new_quiz(self):
        words = ["PYTHON", "ADMIN", "SECURE", "DATA", "HACKER", "CIPHER"]
        word = random.choice(words)
        self.secret_key = random.randint(1, 25)

        # Simple local cipher for quiz generation
        res = ""
        for c in word:
            res += chr((ord(c) - ord('A') + self.secret_key) % 26 + ord('A'))

        self.lbl_challenge.config(text=res)
        self.entry_guess.delete(0, tk.END)
        messagebox.showinfo(
            "Quiz Started", "Puzzle Generated!\n1. Decrypt the text.\n2. Guess the Shift Number.")

    def check_answer(self):
        # 1. Validation: Did they generate a quiz?
        if self.secret_key == 0:
            messagebox.showwarning(
                "Oops", "Please click 'Generate New Challenge' first.")
            return

        # 2. Validation: Is the box empty?
        guess_str = self.entry_guess.get()
        if not guess_str:
            messagebox.showerror("Error", "Please enter a number.")
            return

        try:
            g = int(guess_str)
            if g == self.secret_key:
                self.controller.current_user_score += 10
                self.controller.db.update_score(
                    self.controller.current_user_email, self.controller.current_user_score)
                self.lbl_score.config(
                    text=f"Your Score: {self.controller.current_user_score}")
                messagebox.showinfo(
                    "CORRECT!", f"Good Job! The key was {self.secret_key}.\n+10 Points saved to Database.")
                # Reset for next round
                self.secret_key = 0
                self.lbl_challenge.config(text="[Press Generate]")
                self.entry_guess.delete(0, tk.END)
            else:
                messagebox.showerror("WRONG", "Incorrect key. Try again!")
        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid NUMBER (e.g., 3, 5, 10).")

# ==========================================
# PAGE 5: ADMIN DASHBOARD
# ==========================================


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#ffffff")
        self.controller = controller

        header = tk.Frame(self, bg="#d9534f", pady=15)
        header.pack(fill="x")
        tk.Label(header, text="ADMIN DATABASE PANEL", font=(
            "Arial", 16, "bold"), bg="#d9534f", fg="white").pack()

        # Table (Treeview)
        columns = ("email", "role", "score", "status")
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", height=15)

        self.tree.heading("email", text="User Email")
        self.tree.heading("role", text="Role")
        self.tree.heading("score", text="Quiz Score")
        self.tree.heading("status", text="Online Status")

        self.tree.column("email", width=250)
        self.tree.column("role", width=100)
        self.tree.column("score", width=80)
        self.tree.column("status", width=120)

        self.tree.pack(pady=20, padx=20)

        # Admin Actions
        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔄 Refresh Data", command=self.load_data,
                  bg="#eee", font=("Arial", 10)).pack(side="left", padx=5)
        tk.Button(btn_frame, text="⚡ Promote/Demote User", command=self.toggle_user_role,
                  bg="#ffc107", font=("Arial", 10)).pack(side="left", padx=5)

        tk.Button(self, text="< BACK TO MAIN APP", bg="#333", fg="white", font=("Arial", 10, "bold"),
                  command=lambda: controller.show_frame("MainPage")).pack(pady=20)

    def load_data(self):
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.controller.db.get_all_users()
        for u in users:
            # u = (email, role, score, is_online)
            status_symbol = "🟢 Online" if u[3] == 1 else "🔴 Offline"
            self.tree.insert("", tk.END, values=(
                u[0], u[1], u[2], status_symbol))

    def toggle_user_role(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(
                "Select User", "Please click a user in the list first.")
            return

        item = self.tree.item(selected)
        email = item['values'][0]

        new_role = self.controller.db.toggle_role(email)
        if new_role:
            messagebox.showinfo("Updated", f"{email} is now: {new_role}")
            self.load_data()
        else:
            messagebox.showerror("Error", "Cannot change Super Admin role.")


# --- RUN APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()
