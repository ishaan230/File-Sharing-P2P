import socket
import json
import os
import sys
import requests
from download.utils import get_config
sys.path.append("../")
from central_reg import MongoWrapper


def request_download(fid, seeder):

    get_config()
    timeout_dur = 15
    python_message = {
            "operation": "Request download",
            "file_uid": fid,
            "offset": seeder['offset']
        }
    
    message = json.dumps(python_message)
    SHARE_PATH = os.environ['SHARE_PATH']
    seeder_ip = str(seeder['user_ip'])
    print(seeder_ip)
    seeder_port = int(os.environ['U_PORT'])

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
                        with open(f"{SHARE_PATH}\{python_message['file_uid']}_{int(seeder['offset']) + 3}.txt", "ab+") as file_part:
                            file_part.write(part)
                            return True
                
                part.extend(data)
                
        except Exception as e:
            print(e)
            return False
        
    

def make_download_requests(file_uid):

    # fetch file_info and seeder_info from database using file uid
    get_config()
    mongo = MongoWrapper()
    file_info = mongo.get_file_data(file_uid)
    seeders_info = []
    
    parts_of_file = mongo.get_parts_for_file(file_info["file_uid"])
    
    for part in parts_of_file:
        for user in part['users']:
            user_ip = mongo.get_user_ip(user)
            user_info = { "offset": part['offset'], "user_ip": user_ip }
            seeders_info += [user_info]

    '''
    seeder_info contains the details of the parts and peers that seed them. For now, assume it is an array of objects containing the 
    following properties:
    -file_uid
    -offset
    -user_ip

    and file_info contains :
    -file_name
    -file_uid
    -file_total_parts
    -file_extension
    -size
    '''


    for seeder_info in seeders_info:
            
        #Here will start send http request to Flask server to start concurrent downloads with each each seeder. Will have to refactor.

        request_data = json.dumps({ 'file_uid': file_info['file_uid'], 'seeder_info': seeder_info})
        # request_data = { 'file_uid': file_info['file_uid'], 'seeder_info': seeder_info}
        if requests.post("http://127.0.0.1:5000/download/request", json = request_data).text != "Success":
            return "Something went wrong!"
        else:
            pass
            # mongo.update_seeders_post_download(file_info['file_uid'], seeder_info['offset'])
    
    return "Success!"
        
    

    
def main():
    get_config()
    
    file_info = {
        "file_uid": "1023"
    }  
    
    make_download_requests(file_info['file_uid'])
    

if __name__ == "__main__":
        main()
        


