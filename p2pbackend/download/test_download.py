import socket
import select
import os
import time
from dotenv import load_dotenv
import sys
sys.path.append("../")
from central_reg import MongoWrapper

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

#Code to work with Mongo - add

'''
mongo_cluster = MongoWrapper()
part = {"offset": "0", "file_uid": "1023", "users": ["102"]}
data = mongo_cluster.add_data_to_collection("Part", part) 
print(data)
'''


#Code to work with Mongo - get

mongo_cluster = MongoWrapper()
data = mongo_cluster.get_collection_data("Part") 
for item in data:
    print(item)


#Code for seeder_info query
'''
mongo = MongoWrapper()
file_info = mongo.get_file_data("1023")
seeder_info = []
    
parts_of_file = mongo.get_parts_for_file(file_info["file_uid"])
    
for part in parts_of_file:
  for user in part['users']:
      user_ip = mongo.get_user_ip(user)
      user_info = { "offset": part['offset'], "user_ip": user_ip }
      seeder_info += [user_info]

print(seeder_info)

'''







    