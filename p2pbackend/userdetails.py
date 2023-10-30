import socket
import time

def get_details():
    try:
        # check_existing_user()
        host_details = []
        hostname = socket.gethostname()
        salt = time.time()    
        hostname = hostname + str(salt) 
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
        host_details.append([hostname,ip])

        print(host_details)
    except socket.error as e:
        print(f"Error: {e}")
        return None

# def check_existing_user(host_details):
#     if host_details[0] in host_details:
#         #update ip
#             pass

get_details()