import socket
import time
import central_reg

def get_details():
    try:
        host_details = []
        fetched_data = []
        object = central_reg.MongoWrapper()
        data = object.get_collection_data("Peer")
        for a in data:
            fetched_data.append(a)
        print("Data from DB:")
        print(fetched_data)
        hostname = socket.gethostname()
        salt = time.time()    
        hostname = hostname + str(salt) 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        host_details.append([hostname, ip])
        host_details = [["hostname4","8.8.8.8"]]

        for entry in fetched_data:
            if host_details[0][0] in entry['User_id']:
                print("True")
                update_existing_user(host_details, entry, object)
                print("Done")
                exit()
        
        addnew_details_json = {"User_id": f"{host_details[0][0]}", "IP_Address": f"{host_details[0][1]}"}
        object.add_data_to_collection("Peer", addnew_details_json)
        print("New Details Added")

    except socket.error as e:
        print(f"Error: {e}")
        return None

def update_existing_user(host_details, fetched_entry, object):
    updated_details_json = {"User_id": f"{host_details[0][0]}", "IP_Address": f"{host_details[0][1]}"}
    object.update_data("Peer", fetched_entry, updated_details_json)
    print("Updated")

get_details()
