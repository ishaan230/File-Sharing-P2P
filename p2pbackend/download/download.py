import socket
import json
import os
import select
from utils import get_config



def request_download(fid, offset, seeder):

    timeout_dur = 15
    python_message = {
            "operation": "Request download",
            "file_uid": fid,
            "offset": offset
        }
    
    message = json.dumps(python_message)
    SHARE_PATH = os.environ['SHARE_PATH']
    seeder_ip = seeder['seeder_ip']
    seeder_port = int(seeder['seeder_port'])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((seeder_ip, seeder_port))
        sock.settimeout(timeout_dur) #Last argument is timeout in seconds.
        print("Connected to sender!")
        
        sock.sendall(bytes(message, encoding='utf-8'))
        print("Sent request")
        
        try:
            ack = sock.recv(1024).decode('utf-8')
            print(ack)
            
            part = bytearray()
            
            while True:
                print("Receiving part...")
                data = sock.recv(1024)
                
                if not data:
                        with open(f"{SHARE_PATH}\{python_message['file_uid']}_{offset + 1}.txt", "wb+") as file_part:
                            file_part.write(part)
                            return True
                    # print(part)
                    # return True
                
                part.extend(data)
                
        except Exception as e:
            print(e)
            return False
            
        

def make_download_requests(file_info, seeder_info):

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
            if request_download(file_info, part_req, seeder):
                print("Sent message to seeder!")
            else:
                print("something went wrong!!")

    
def main():
    get_config()

    LOCALHOST_IP = os.environ['LOCAL_IP']
    HOST_PORT = os.environ['U_PORT']
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

    request_download(file_info['file_uid'], 0, seeders_info[0])
    

if __name__ == "__main__":
        main()
        


