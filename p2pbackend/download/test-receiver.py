import socket
import json

def main():
    LOCALHOST_IP = '127.0.0.1'
    HOST_PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((LOCALHOST_IP, HOST_PORT))
        sock.listen()
        conn_sock, addr = sock.accept()
        json_message = b''
        with conn_sock:
            while True:
                data = conn_sock.recv(1024)
                json_message += data
                if not data:
                    json_message = json_message.decode("utf-8")
                    json_message = json.loads(json_message)
                    print(json_message)
                    break

if __name__ == "__main__":
    main()
