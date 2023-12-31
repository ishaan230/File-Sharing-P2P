import socket
import central_reg
import uuid


def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip


def get_details():
    print("GET details")
    try:
        mac = uuid.getnode()
        host_details = []
        fetched_data = []
        object = central_reg.MongoWrapper()
        data = object.get_collection_data("Peer")
        for a in data:
            fetched_data.append(a)
        print("Data from DB:")
        print(fetched_data)
        hostname = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        print(hostname)
        # salt = time.time()    
        # hostname = hostname + str(salt) 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        host_details.append([hostname, ip, True])
        for entry in fetched_data:
            if host_details[0][0] in entry['User_id']:
                print("True")
                update_existing_user(host_details, entry, object)
                print("Done")
                return True
        
        addnew_details_json = {"User_id": f"{host_details[0][0]}", "IP_Address": f"{host_details[0][1]}", "active": True}
        object.add_data_to_collection("Peer", addnew_details_json)
        print("New Details Added")
        return True

    except socket.error as e:
        print(f"Error: {e}")
        return None


def set_user_inactive():
    print("GET details")
    try:
        mac = uuid.getnode()
        host_details = []
        fetched_data = []
        object = central_reg.MongoWrapper()
        data = object.get_collection_data("Peer")
        for a in data:
            fetched_data.append(a)
        print("Data from DB:")
        print(fetched_data)
        hostname = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
        print(hostname)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        host_details.append([hostname, ip, False])
        for entry in fetched_data:
            if host_details[0][0] in entry['User_id']:
                print("True")
                update_existing_user(host_details, entry, object)
                print("Done")
                return True
        addnew_details_json = {"User_id": f"{host_details[0][0]}", "IP_Address": f"{host_details[0][1]}", "active": False}
        object.add_data_to_collection("Peer", addnew_details_json)
        print("New Details Added")
        return True

    except socket.error as e:
        print(f"Error: {e}")
        return None


def update_existing_user(host_details, fetched_entry, object):
    print("ADDINGGGGg-> ", host_details)
    updated_details_json = {"User_id": f"{host_details[0][0]}", "IP_Address": f"{host_details[0][1]}", "active": host_details[0][2]}
    print(updated_details_json)
    object.update_data("Peer", fetched_entry, updated_details_json)
    print("Updated")

# get_details()
