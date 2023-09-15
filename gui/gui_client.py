import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import time

# Function to receive a text file from the server
def receive_file():
    ip = ip_entry.get()
    port = int(port_entry.get())
    filename = file_entry.get()
    filename += ".txt"
    HOST = ip  # The server's IP address
    PORT = port  # The port used by the server

    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"This message was sent by the client")
        data = s.recv(1024)

    with open(filename, "wb") as file:
        file.write(data)
        print("Received!")
    
    messagebox.showinfo("showinfo", "Received File")

    result_label.config(text=f"File received: {filename}")
    time.sleep(2)
    exit()

# Create a GUI window
window = tk.Tk()
window.title("File Receiver")
window.geometry("400x300")  # Set the window size

# Create a style for ttk widgets
style = ttk.Style()
style.configure("TButton", padding=6, relief="flat", background="white", foreground="#4CAF50")
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TEntry", font=("Helvetica", 12))

# IP Address Label and Entry
ip_label = ttk.Label(window, text="Server IP Address:")
ip_label.pack(pady=10)
ip_entry = ttk.Entry(window)
ip_entry.pack()

# Port Number Label and Entry
port_label = ttk.Label(window, text="Port Number:")
port_label.pack(pady=10)
port_entry = ttk.Entry(window)
port_entry.pack()

# File Name Label and Entry
file_label = ttk.Label(window, text="File Name:")
file_label.pack(pady=10)
file_entry = ttk.Entry(window)
file_entry.pack()

# Receive Button
receive_button = ttk.Button(window, text="Receive File", command=receive_file)
receive_button.pack(pady=20)

# Result Label
result_label = ttk.Label(window, text="")
result_label.pack()

window.mainloop()
