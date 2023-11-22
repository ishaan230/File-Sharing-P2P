import socket
import select
import os
import time
from dotenv import load_dotenv

load_dotenv()

LOCAL_IP = os.environ['LOCAL_IP']
PORT = int(os.environ['D_PORT'])
SHARE_PATH = os.environ['SHARE_PATH']
delay_time = 2

#Code for select call
'''
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((LOCAL_IP, PORT))
    sock.setblocking(0)
    ready = select.select([sock], [], [], 10)
    print(ready)
    if ready[0]:
        message = sock.recv(1024)
        with open(f"{SHARE_PATH}\hello.part", "wb+") as openfile:
            openfile.write(message)
    else:
        print("Something went wrong")
'''

#Code to simulate timeout
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((LOCAL_IP, PORT))
    sock.settimeout(delay_time)
    print("Connected to sender")
    
    print("Sent message")
    sock.sendall(b'Hello World')
    
    echo = sock.recv(1024).decode('utf-8')
    print(echo)
    