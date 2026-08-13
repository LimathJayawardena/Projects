# 🛡️ Secure Cipher System & Cipher Tool
**Group D Project**

![Project Status](https://img.shields.io/badge/Status-100%25%20Complete-green)
![Python Version](https://img.shields.io/badge/Python-3.0-blue)
![Framework](https://img.shields.io/badge/Framework-Flet-orange)

Welcome to the **Secure Cipher System**! This project is a Python-based educational tool designed to demonstrate encryption logic and modern GUI development. It features a working Caesar Cipher game and a custom Sign-in interface.

---

## 📊 Project Progress
**Current Status:** Building the UI & Logic [■■■■■■■■■■] 100% Complete

## 📁 Project Structure

* **`cc_tool_app.py`**: 🖼️ The Graphical User Interface (GUI). Handles the Sign-in page, user inputs (Email, Username), and responsive layout using **Flet Controls**.
* **`caesar_cipher.py`**: 🧠 The "Brain" of the app. Contains the math logic for scrambling words, calculating points, and managing game rounds.

---

## 🌟 Key Features

* **🔐 User Authentication UI:** A professional sign-in screen built with modern material design components and custom styling.
* **🎲 Random Logic:** The system picks random words (e.g., *digit*, *cipher*, or *python*) and applies a random shift.
* **🔄 Modular Arithmetic:** Uses the `% 26` math trick to ensure letters always "wrap around" (Z becomes A).
* **🎮 Scoring System:** Tracks user progress through 10 rounds of decryption challenges.

---

## 🚀 How it Works (The Logic)

The encryption in `caesar_cipher.py` follows this mathematical logic:

1.  **Character Conversion**: It takes a letter and converts it to a number using `ord()`.
2.  **Secret Shift**: It adds a secret `shift` value to that number.
3.  **The Wrap-Around**: It uses the modulo operator `% 26` to keep the result within the alphabet.
4.  **Re-conversion**: It converts the number back to a letter using `chr()`.

**Mathematical Formula:** $E_n(x) = (x + n) \mod 26$



---

## 🛠️ Built With

* **Language:** Python 3 🐍
* **GUI Framework:** [Flet](https://flet.dev/) (Flutter for Python)
* **Logic Modules:** `random`, `string`

---

<div align="center">
  <b>Developed by Limath Jayawardena</b>
</div>
