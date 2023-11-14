import socket
import json
import os
from utils import get_config

def listen_download_req():
    LOCALHOST_IP = os.environ['LOCAL_IP']
    HOST_PORT = int(os.environ['U_PORT'])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((LOCALHOST_IP, HOST_PORT))
        sock.listen()
        conn_sock, addr = sock.accept()
        print("Accepted connection!")
        json_message = b''
        with conn_sock:
            data = conn_sock.recv(1024)
            json_message = json_message.decode("utf-8")
            request = json.loads(json_message)
            conn_sock.sendall(b"Received request, sending part...")
            
            json_message += data
            print("Receiving data..")

def send_part(request, sock):
    SHARE_PATH = os.environ['SHARE_PATH']
    file_uid = request['file_uid']
    offset = request['offset']
    part_path = f"{SHARE_PATH}\{file_uid}_{offset}.part"
        
    print(file_uid, offset, part_path)

    #Assume that files parts are available individually as well 
    with open(part_path, "rb") as file_to_send:
        part_content = file_to_send.read()
        conn_sock.sendall(part_content)

    print("Sent part!")

    
def main():
    get_config()
    listen_download_req()

if __name__ == "__main__":
    main()
