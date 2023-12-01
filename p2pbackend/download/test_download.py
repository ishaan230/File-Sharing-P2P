import socket
import os
import base64
from dotenv import load_dotenv
import sys
sys.path.append("../")
from central_reg import MongoWrapper
from file_utils import break_file
load_dotenv()

# LOCAL_IP = os.environ['LOCAL_IP']
# PORT = int(os.environ['D_PORT'])
# SHARE_PATH = os.environ['SHARE_PATH']
# delay_time = 2

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
'''
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((LOCAL_IP, PORT))
    sock.settimeout(delay_time)
    print("Connected to sender")
    
    print("Sent message")
    sock.sendall(b'Hello World')
    
    echo = sock.recv(1024).decode('utf-8')
    print(echo)
'''

def simulate_upload():
    SHARE_PATH = os.environ['UPLOAD_SHARE_PATH']
    file_name = "witcher"
    filepath = SHARE_PATH + f"\{file_name}.jpeg"
    extension = filepath.split("\\")[-1].split(".")[-1]
    chunk = 10 * 1024
    chunks = []
    hash = '29112003'
    parts = break_file(filepath, chunk)
    for i in range(len(parts)):
        partpath = SHARE_PATH + f"\{hash}_{i}.txt"
        print(partpath)
        with open(partpath, "w+") as part_file:
            part_file.write(parts[i])
            chunks += [sys.getsizeof(parts[i])]
    
    
    mongo = MongoWrapper()
    file = {'hash': hash, 'num_parts': len(parts), 'size': sum(chunks), 'type': extension, 'name': file_name}
    result = mongo.add_data_to_collection("File", file)
    print("File Object ID", result)
    
    for i in range(len(parts)):
        part = {'offset': str(i), 'file_id': hash, 'size': chunks[i], 'users': ['102']}
        result = mongo.add_data_to_collection("Part", part)
        print("Part Object ID", i, result)
    
def simulate_download():
    DOWNLOAD_SHARE_PATH = os.environ['DOWNLOAD_SHARE_PATH']
    UPLOAD_SHARE_PATH = os.environ['UPLOAD_SHARE_PATH']
    total_parts = 5
    hash = '29112003'
    extension = ".jpeg"
    file_name = "witcher"
    
    file_content = b''
    for i in range(total_parts):
        with open(UPLOAD_SHARE_PATH + f"\{hash}_{i}.txt", "r") as part_file:
            content = part_file.read()
            content = base64.b64decode(content.encode('utf-8'))
            file_content += content
            
    with open(DOWNLOAD_SHARE_PATH + f"\{hash}.{extension}", "wb+") as file:
        file.write(file_content)
    
    
def main():
    # simulate_upload()
    # simulate_download()
    
    #Code to work with Mongo - add

    # mongo_cluster = MongoWrapper()
    # part = {'offset': '0', 'file_uid': '1023', 'size': 96, 'users': ['102']}
    # data = mongo_cluster.add_data_to_collection("Part", part) 
    # print(data)


    # Code to work with Mongo - get

    # mongo_cluster = MongoWrapper()
    # data = mongo_cluster.get_collection_data("Peer") 
    # for item in data:
    #     print(item)

    # Code to work with mongo - delete
    # mongo = MongoWrapper()
    # result = mongo.delete_part("1023", "0")
    # print(result)

    # Code to work with mongo - update
    # mongo = MongoWrapper()
    # result = mongo.update_data("File", {"hash": '1023'}, {'num_parts': 2})
    # print(result)

    # Code for seeder_info query

    mongo = MongoWrapper()
    file_info = mongo.get_file_data("29112003")
    print(file_info)
    seeder_info = []
        
    parts_of_file = mongo.get_parts_for_file(file_info["hash"])
        
    for part in parts_of_file:
        print(part)
        for user in part['users']:
            user_ip = mongo.get_user_ip(user)
            user_info = { "offset": part['offset'], "user_ip": user_ip }
            seeder_info += [user_info]
    

    print(seeder_info)


if __name__ == "__main__":
    main()









    