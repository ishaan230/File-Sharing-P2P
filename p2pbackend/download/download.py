import socket
import json

def receive_download():
    pass

def make_download_request(file_info, seeder_info):

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

    hostname = socket.gethostname()
    HOST_IP = socket.gethostbyname(hostname)
    print(HOST_IP)
    

    for part_req in range(0, file_info["file_total_parts"]):

        python_message = {
            "operation": "Request download",
            "file_uid": file_info["file_uid"],
            "offset": part_req
        }
        message = json.dumps(python_message)

        seeders_for_part = filter(lambda seeder: seeder["offset"] == part_req, seeder_info)

        for seeder in seeders_for_part:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((seeder["seeder_ip"], seeder["seeder_port"]))
                sock.sendall(bytes(message, encoding='utf-8'))
            print("Sent message to seeder!")

    
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
    main()


