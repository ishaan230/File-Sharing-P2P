import socket

host_ip = input("Enter ip: ")
HOST = host_ip  
PORT = 65432  # Port to listen on 

# Text file reading
f = open("send_file.txt", "r")
a = f.readlines()

# Data conversion and String with encoding 'utf-8' 
stri = ""
for i in a:
    stri += i
arr = bytes(stri, 'utf-8')

# Connect to Client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(arr)

