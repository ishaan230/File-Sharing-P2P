import socket
import json
import os
import select
from dotenv import load_dotenv

def get_config():
    try:
        load_dotenv()
        return True
    except Exception:
        print("Could not load configuration")
        return False

def receive_download(file_info, offset, seeder):

    python_message = {
            "operation": "Request download",
            "file_uid": file_info["file_uid"],
            "offset": offset
        }
    
    message = json.dumps(python_message)
    SHARE_PATH = os.environ['SHARE_PATH']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((seeder["seeder_ip"], seeder["seeder_port"]))
        sock.sendall(bytes(message, encoding='utf-8'))
        
        sock.setblocking(0)

        ready = select.select([sock], [], [], 50) #Last argument is timeout in seconds.
        if  ready[0]:
            part = b''
            while True:
                data = sock.recv(1024)
                part += data
                if not data:
                    with open(f"{SHARE_PATH}\{offset}.part", "wb+") as file_part:
                        file_part.write(part)
                    return True
        else:
            return False
        

def make_download_request(file_info, seeder_info):

    #fetch file_info and seeder_info from database using file uid

    '''
    seeder_info contains the details of the parts and peers that seed them. For now, assume it is an array of objects containing the 
    following properties:
    -file_uid
    -offset
    -seeder_ip
    -seeder_port

    and file_info contains :
    -file_name
    -file_uid
    -file_total_parts
    -file_extension
    '''

    for part_req in range(0, file_info["file_total_parts"]):

        seeders_for_part = filter(lambda seeder: seeder["offset"] == part_req, seeder_info)

        for seeder in seeders_for_part:
            #Here will start send http request to Flask server to start concurrent downloads with each each seeder. Will have to refactor.
            if receive_download(file_info, part_req, seeder):
                print("Sent message to seeder!")
            else:
                print("something went wrong!!")

    
def main():
    LOCALHOST_IP = '127.0.0.1'
    HOST_PORT = 12345
    file_info = {
        "file_uid": 1,
        "file_total_parts": 1,
        "file_name": "file",
        "file_extension": ".py"
    }  
    seeders_info = [{
        "file_uid": 1,
        "offset": 0,
        "seeder_ip": LOCALHOST_IP,
        "seeder_port": HOST_PORT
    }]
    make_download_request(file_info, seeders_info)

if __name__ == "__main__":
        get_config()
        # receive_download()


