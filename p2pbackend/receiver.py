import socket

server_ip = input("Enter IP to connect : ")
server_port = int(input("Enter Port to connect: "))
HOST = server_ip  # The client1's IP address
PORT = server_port  # The port used by the client1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"This message was sent by the client")
    data = s.recv(1024)

with open("recieved_file.txt", "wb") as file:
    file.write(data)
    print("Received !")


