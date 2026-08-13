import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import socket
import threading
import json
import urllib.request
import urllib.parse
import base64
import random

PORT = 9999
HEADER = 4096
FORMAT = 'utf-8'

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    try:
        s = int(shift) if mode == 'encrypt' else -int(shift)
    except:
        return text

    for char in text:
        if char.isalpha():
            start = ord('a') if char.islower() else ord('A')
            result += chr((ord(char) - start + s) % 26 + start)
        else:
            result += char
    return result

def to_morse(text):
    MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...',
             'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----', ' ': '/'}
    return ' '.join(MORSE.get(char.upper(), char) for char in text)

def from_morse(text):
    MORSE = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--',
             'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', ' ': '/'}
    REVERSED = {v: k for k, v in MORSE.items()}
    return ''.join(REVERSED.get(code, '') for code in text.split(' '))

def scramble_logic(text, shift, mode='encrypt'):
    try:
        s_val = int(shift)
    except:
        return text

    n = len(text)
    indices = list(range(n))
    random.seed(s_val)
    random.shuffle(indices)

    if mode == 'encrypt':
        shifted_text = caesar_cipher(text, s_val, 'encrypt')
        result = [""] * n
        for i, idx in enumerate(indices):
            result[idx] = shifted_text[i]
        return "".join(result)
    else:
        unscrambled = [""] * n
        for i, idx in enumerate(indices):
            try:
                unscrambled[i] = text[idx]
            except IndexError:
                return "Error"
        return caesar_cipher("".join(unscrambled), s_val, 'decrypt')

def multilayer_encrypt(text, shift):
    step1 = caesar_cipher(text, shift, 'encrypt')
    step2 = base64.b64encode(step1.encode("utf-8")).decode("utf-8")
    return step2

def multilayer_decrypt(encoded_text, shift):
    try:
        step1 = base64.b64decode(encoded_text).decode('utf-8')
        step2 = caesar_cipher(step1, shift, 'decrypt')
        return step2
    except:
        return "Error"

class CipherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cipher App")
        self.geometry("1100x900")
        self.configure(bg="#050505")
        
        self.server = None
        self.client = None
        self.clients_data = {}
        self.my_codename = "Unknown"
        self.qr_ref = None

        self.show_menu()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"

    def show_menu(self):
        self.clear_screen()
        frame = tk.Frame(self, bg="#050505")
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text="SECURE CHAT", font=("Arial", 20, "bold"), fg="#00FF41", bg="#050505").pack(pady=20)
        
        tk.Button(frame, text="HOST (SERVER)", font=("Arial", 14), bg="green", fg="white", width=25, command=self.start_server).pack(pady=10)
        tk.Button(frame, text="JOIN (CLIENT)", font=("Arial", 14), bg="blue", fg="white", width=25, command=self.show_join).pack(pady=10)

    def start_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(('0.0.0.0', PORT))
            self.server.listen()
            threading.Thread(target=self.accept_clients, daemon=True).start()
            self.show_host_ui(self.get_ip())
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def accept_clients(self):
        while True:
            try:
                conn, addr = self.server.accept()
                threading.Thread(target=self.handshake, args=(conn, addr), daemon=True).start()
            except:
                break

    def handshake(self, conn, addr):
        try:
            name = conn.recv(HEADER).decode(FORMAT)
            self.clients_data[addr] = {"conn": conn, "name": name}
            self.update_client_list()
        except:
            conn.close()

    def update_client_list(self):
        try:
            self.client_box.delete(0, tk.END)
            for addr, data in self.clients_data.items():
                self.client_box.insert(tk.END, f"{data['name']} ({addr[0]})")
        except:
            pass

    def show_host_ui(self, ip):
        self.clear_screen()
        
        tk.Label(self, text=f"HOST IP: {ip}", bg="#050505", fg="#00FF41", font=("Arial", 14)).pack(pady=10)

        main_frame = tk.Frame(self, bg="#050505")
        main_frame.pack(fill="both", expand=True, padx=20)

        left_frame = tk.LabelFrame(main_frame, text="Connected Users", bg="#050505", fg="white")
        left_frame.pack(side="left", fill="y", padx=10)
        
        self.client_box = tk.Listbox(left_frame, bg="#111", fg="#00FF41", width=30)
        self.client_box.pack(fill="both", expand=True)

        right_frame = tk.LabelFrame(main_frame, text="Send Message", bg="#050505", fg="white")
        right_frame.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(right_frame, text="Message:", bg="#050505", fg="white").pack(anchor="w")
        self.msg_entry = tk.Entry(right_frame, bg="#222", fg="white", font=("Arial", 12))
        self.msg_entry.pack(fill="x", pady=5)

        tk.Label(right_frame, text="Shift Key (Number):", bg="#050505", fg="white").pack(anchor="w")
        self.shift_entry = tk.Entry(right_frame, bg="#222", fg="white", font=("Arial", 12))
        self.shift_entry.insert(0, "5")
        self.shift_entry.pack(fill="x", pady=5)

        tk.Label(right_frame, text="Select Encryption Method:", bg="#050505", fg="white").pack(anchor="w", pady=(10, 0))
        self.method_combo = ttk.Combobox(right_frame, values=["Caesar Cipher", "Morse Code", "Multilayer", "Scramble", "QR Code"], state="readonly")
        self.method_combo.current(0)
        self.method_combo.pack(fill="x", pady=5)

        tk.Button(right_frame, text="SEND SELECTED", bg="#003300", fg="#00FF41", command=self.send_msg).pack(fill="x", pady=10)
        
        self.log_box = tk.Text(right_frame, height=10, bg="#111", fg="#00FF41")
        self.log_box.pack(fill="x", pady=10)

        tk.Button(self, text="EXIT", bg="red", fg="white", command=self.close_all).pack(pady=5)

    def send_msg(self):
        selection = self.client_box.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Select a user first")
            return
        
        raw_msg = self.msg_entry.get()
        if not raw_msg: return
        
        shift = self.shift_entry.get()
        method = self.method_combo.get()
        
        payload = {"method": method, "data": "", "qr": "", "shift": shift}

        if method == "Caesar Cipher":
            payload["data"] = f"{caesar_cipher(raw_msg, shift, 'encrypt')} {shift}"
        elif method == "Morse Code":
            payload["data"] = to_morse(raw_msg)
        elif method == "Multilayer":
            payload["data"] = multilayer_encrypt(raw_msg, shift)
        elif method == "Scramble":
            payload["data"] = f"{scramble_logic(raw_msg, shift, 'encrypt')} {shift}"
        elif method == "QR Code":
            payload["qr"] = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(raw_msg)}"

        target_key = list(self.clients_data.keys())[selection[0]]
        conn = self.clients_data[target_key]['conn']
        
        try:
            conn.send(json.dumps(payload).encode(FORMAT))
            self.log_box.insert(tk.END, f"Sent ({method}): {raw_msg}\n")
            self.msg_entry.delete(0, tk.END)
        except:
            pass

    def show_join(self):
        self.clear_screen()
        frame = tk.Frame(self, bg="#050505")
        frame.pack(pady=50)

        tk.Label(frame, text="Name:", bg="#050505", fg="white").pack()
        name_entry = tk.Entry(frame, width=30)
        name_entry.pack(pady=5)

        tk.Label(frame, text="Host IP:", bg="#050505", fg="white").pack()
        ip_entry = tk.Entry(frame, width=30)
        ip_entry.pack(pady=5)
        ip_entry.insert(0, self.get_ip())

        def connect():
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((ip_entry.get(), PORT))
                self.client.send(name_entry.get().encode(FORMAT))
                self.my_codename = name_entry.get()
                threading.Thread(target=self.receive_loop, daemon=True).start()
                self.show_client_ui()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame, text="CONNECT", bg="blue", fg="white", command=connect).pack(pady=20)
        tk.Button(frame, text="BACK", command=self.show_menu).pack()

    def receive_loop(self):
        while True:
            try:
                msg = self.client.recv(HEADER).decode(FORMAT)
                if msg:
                    data = json.loads(msg)
                    self.after(0, lambda: self.update_inbox(data))
                else:
                    break
            except:
                break

    def show_client_ui(self):
        self.clear_screen()
        tk.Label(self, text=f"User: {self.my_codename}", bg="#050505", fg="blue", font=("Arial", 14)).pack(pady=10)
        
        main_frame = tk.Frame(self, bg="#050505")
        main_frame.pack(fill="both", expand=True, padx=20)

        inbox_frame = tk.LabelFrame(main_frame, text="Incoming Intel", bg="#050505", fg="white")
        inbox_frame.pack(fill="x", pady=5)

        self.box_caesar = self.create_display_box(inbox_frame, "Caesar Cipher", "#FF3333")
        self.box_morse = self.create_display_box(inbox_frame, "Morse Code", "#FFFF33")
        self.box_scramble = self.create_display_box(inbox_frame, "Scrambled", "#CC33FF")
        self.box_multi = self.create_display_box(inbox_frame, "Multilayer", "#FFA500")

        self.qr_label = tk.Label(inbox_frame, text="[Waiting for QR]", bg="#050505", fg="grey")
        self.qr_label.pack(pady=5)

        tools_frame = tk.LabelFrame(main_frame, text="Decryption Generators (Helper)", bg="#050505", fg="white")
        tools_frame.pack(fill="both", expand=True)

        nb = ttk.Notebook(tools_frame)
        nb.pack(fill="both", expand=True)

        self.add_tool_tab(nb, "Caesar", self.smart_caesar)
        self.add_tool_tab(nb, "Multilayer", lambda t, s: multilayer_decrypt(t, s))
        self.add_tool_tab(nb, "Morse", lambda t, s: from_morse(t))
        self.add_tool_tab(nb, "Scramble", self.smart_scramble)

        tk.Button(self, text="DISCONNECT", bg="red", fg="white", command=self.close_all).pack(pady=5)

    def create_display_box(self, parent, title, color):
        tk.Label(parent, text=title, bg="#050505", fg="grey").pack(anchor="w")
        box = tk.Text(parent, height=2, bg="#111", fg=color)
        box.pack(fill="x", padx=5, pady=2)
        return box

    def add_tool_tab(self, notebook, name, logic_func):
        frame = tk.Frame(notebook, bg="#111")
        notebook.add(frame, text=name)
        
        inp = tk.Text(frame, height=3, bg="#222", fg="white")
        inp.pack(pady=5)
        
        shift = tk.Entry(frame, bg="#222", fg="white")
        shift.pack()
        shift.insert(0, "5")
        
        res = tk.Text(frame, height=3, bg="black", fg="green")
        res.pack(pady=5)

        def run():
            val = logic_func(inp.get("1.0", tk.END).strip(), shift.get())
            res.delete("1.0", tk.END)
            res.insert("1.0", val)

        tk.Button(frame, text="DECRYPT", command=run).pack()

    def smart_caesar(self, text, shift):
        parts = text.split()
        if len(parts) >= 2 and parts[-1].isdigit():
            real_text = " ".join(parts[:-1])
            real_shift = parts[-1]
            return caesar_cipher(real_text, real_shift, 'dec')
        return caesar_cipher(text, shift, 'dec')

    def smart_scramble(self, text, shift):
        parts = text.split()
        if len(parts) >= 2 and parts[-1].isdigit():
            real_text = " ".join(parts[:-1])
            real_shift = parts[-1]
            return scramble_logic(real_text, real_shift, 'dec')
        return scramble_logic(text, shift, 'dec')

    def update_inbox(self, data):
        self.box_caesar.delete("1.0", tk.END)
        self.box_morse.delete("1.0", tk.END)
        self.box_scramble.delete("1.0", tk.END)
        self.box_multi.delete("1.0", tk.END)
        self.qr_label.config(image='', text="[Waiting for QR]")
        self.qr_ref = None

        method = data.get("method")
        content = data.get("data")

        if method == "Caesar Cipher":
            self.box_caesar.insert("1.0", content)
        elif method == "Morse Code":
            self.box_morse.insert("1.0", content)
        elif method == "Multilayer":
            self.box_multi.insert("1.0", content)
        elif method == "Scramble":
            self.box_scramble.insert("1.0", content)
        elif method == "QR Code":
            threading.Thread(target=self.load_qr, args=(data['qr'],), daemon=True).start()

        messagebox.showinfo("New Message", f"Received {method} Data")

    def load_qr(self, url):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as u:
                raw_data = u.read()
                b64_data = base64.b64encode(raw_data)
                
            def update():
                self.qr_ref = PhotoImage(data=b64_data)
                self.qr_label.config(image=self.qr_ref, text="")
            self.after(0, update)
        except:
            pass

    def close_all(self):
        if self.server: self.server.close()
        if self.client: self.client.close()
        self.destroy()

if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()