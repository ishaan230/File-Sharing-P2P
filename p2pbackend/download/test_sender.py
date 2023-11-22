import socket
import select
import os
import time
from dotenv import load_dotenv

load_dotenv()

LOCAL_IP = os.environ['LOCAL_IP']
PORT = int(os.environ['D_PORT'])
message = b"Hello world!"
timeout_dur = 5

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_sock:
    listen_sock.bind((LOCAL_IP, PORT))
    listen_sock.settimeout(timeout_dur)
    try:
        listen_sock.listen()
        print("Socket Listening")
        
        sock, addr = listen_sock.accept()
        sock.settimeout(timeout_dur)
        print("Connection accepted!")
        
        with sock:
            message = sock.recv(1024).decode('utf-8')
            print(message)
            time.sleep(timeout_dur)
            sock.sendall(bytes(message, encoding='utf-8'))
            
    except Exception as e:
        print("Socket timed out!")
    
        
            
            