import socket


class Sender:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip_addr = socket.gethostbyname(self.hostname)
        self.port = 65432
        self.alt_port = 54321

    def read_file(self, file_path):
        content = None
        with open(file_path, "r") as file:
            content = file.read()
            file.close()
        if content:
            return bytes(content, 'utf-8')
        return None

    def setup_listener(self):
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sckt.bind((self.ip_addr, self.port))
        except OSError:
            sckt.bind((self.ip_addr, self.alt_port))
        else:
            return None
        return sckt

    def send_message(self, client_addr, content):
        sckt = self.setup_listener()
        if sckt:
            print(client_addr)
            sckt.connect(client_addr)
            res = sckt.send(content)
            sckt.close()
            print(res)
        else:
            raise RuntimeError("Unable to bind socket")

    def upload_file(self, file_path, peers):
        content = self.read_file(file_path)
        for peer in peers:
            self.send_message(peer, content)
        print("Sent")


sender = Sender()
msg = b"Hellooo"
sender.send_message(('0.0.0.0', 8000), msg)
