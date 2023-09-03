import socket

server_ip = input("Enter Server IP: ")
server_port = int(input("Enter Server Port: "))
HOST = server_ip  # The server's hostname or IP address
PORT = server_port  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"This message was sent by the client")
    data = s.recv(1024)

with open("recieved_file.txt", "wb") as file:
    file.write(data)
    print("Received !")


