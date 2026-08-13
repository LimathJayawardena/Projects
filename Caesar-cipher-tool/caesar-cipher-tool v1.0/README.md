Secure Cipher System

Group D Project
Made by L.R.Jayawardena

Overview
This is a secure, Python-based desktop application designed for educational purposes in cybersecurity. It features a complete authentication system (Login/Signup/Forgot Password), a Caesar Cipher tool for encryption/decryption, a gamified quiz mode with persistent scoring, and a powerful Admin Dashboard for managing users.

Features
1. User Authentication
Secure Login: Users must authenticate with email and password to access the tool.
Signup: New users can create accounts which are stored in a local SQLite database.
Forgot Password: A feature to reset passwords if forgotten.

2. Role-Based Access Control (RBAC)
The system supports multiple user roles:
Visitor: Standard users who can use the Cipher Tool and Quiz.
Admin: Users with elevated privileges who can access the database panel.
Super Admin: A hardcoded master account (admin@gmail.com) that cannot be deleted or demoted.

3. Cipher Tool
Encryption: Converts plain text into ciphertext using the Caesar Cipher algorithm with a custom shift key.
Decryption: Reverses the process to reveal the original message.

4. Gamified Quiz Mode
Challenge Generation: Randomly generates encrypted messages.
Scoring: Users earn points for correctly guessing the shift key used in the encryption.
Persistence: Scores are saved to the database and persist across sessions.

5. Admin Dashboard
User Management: View a list of all registered users.
Live Status: See who is currently "Online" (Green) or "Offline" (Red).
Role Management: Promote Visitors to Admins or demote Admins to Visitors.
Score Monitoring: View the quiz scores of all users.

How to Run
Install Python: Ensure you have Python installed on your computer.
Download the Code: Save the provided Python code as advanced_cipher.py.
Run the Application:
Open your terminal or command prompt and run:
python advanced_cipher.py

Database: The app will automatically create a file named app_data.db in the same folder to store all data.

Usage Guide
Getting Started
Launch the app.
Click "Create New Account" to register.
Login with your new credentials.
Accessing Admin Features
To access the Admin Panel, you must be an Admin.
Super Admin Login:
Email: admin@gmail.com

Usage Guide
Getting Started Launch the app.
Click "Create New Account" to register.
Login with your new credentials.
Accessing Admin Features
To access the Admin Panel, you must be an Admin.
Super Admin Login:
Email: admin@gmail.com
Password: (Create this account via Signup first!)
Once logged in as an Admin, click the red "🔒 OPEN ADMIN DB" button on the main screen.
Resetting Password
Click "Forgot Password?" on the login screen.
Enter your registered email and a new password.
Click "Update Password".
Educational Tool for Cybersecurity Fundamentals.
Password: (Create this account via Signup first!)
Once logged in as an Admin, click the red "🔒 OPEN ADMIN DB" button on the main screen.
Resetting Password
Click "Forgot Password?" on the login screen.
Enter your registered email and a new password.
Click "Update Password".
Educational Tool for Cybersecurity Fundamentals.
