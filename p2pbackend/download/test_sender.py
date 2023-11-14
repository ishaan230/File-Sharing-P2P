import socket
import select
import os
from dotenv import load_dotenv

load_dotenv()

LOCAL_IP = os.environ['LOCAL_IP']
PORT = int(os.environ['D_PORT'])
message = b"Hello world!"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.connect((LOCAL_IP, PORT))
    sock.sendall(message)