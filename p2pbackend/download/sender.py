import socket
import json
import os
import sys
import base64
from utils import get_config

def listen_download_req():
    LOCALHOST_IP = os.environ['LOCAL_IP']
    HOST_PORT = int(os.environ['U_PORT'])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        
        sock.bind((LOCALHOST_IP, HOST_PORT))
        sock.listen(20)
        print("Listening for requests...")
        
        conn_sock, addr = sock.accept()
        print("Accepted connection!")
        
        with conn_sock:
            data = conn_sock.recv(1024).decode('utf-8')
            request = json.loads(data)
            try:
                conn_sock.sendall(b"Download Request Acknowledged")
                send_part(request, conn_sock)
            except Exception:
                print("Unable to send file part!")
            
                
                
                

def send_part(request, sock):
    SHARE_PATH = os.environ['UPLOAD_SHARE_PATH']
    file_uid = request['file_uid']
    offset = request['offset']
    part_path = f"{SHARE_PATH}\{file_uid}_{offset}.txt"

    # #Assume that files parts are available individually as well 
    with open(part_path, "r") as file_to_send:
        content = file_to_send.read()
        part_content = bytes(content, encoding= 'utf-8')
        print(type(part_content))
        sock.sendall(part_content)

    print("Sent part!")

    
def main():
    get_config()
    while True:
        listen_download_req()

if __name__ == "__main__":
    main()
