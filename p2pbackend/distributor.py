import socket
import math


class Sender:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip_addr = socket.gethostbyname(self.hostname)
        self.port = 65432
        self.alt_port = 54321

    def read_file(self, file_path):
        content = None
        with open(file_path, "rb") as file:
            content = file.read()
            file.close()
        if content:
            return content
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

    def send_message(self, sckt, client_addr, content):
        if sckt:
            print(client_addr)
            sckt.connect(client_addr)
            res = sckt.send(content)
            sckt.close()
            print(res)
        else:
            raise RuntimeError("Unable to bind socket")

    def break_file(self, file_path):
        content = self.read_file(file_path)

        if content:
            part_size = 1024
            parts = []
            cntr = 0
            wrd = ''
            for a in content:
                if cntr == part_size:
                    parts.append(wrd)
                    cntr = 1
                    wrd = str(a)
                wrd += str(a)
                cntr += 1
            print(wrd)

    def upload_file(self, file_path, peers):
        sckt = self.setup_listener()
        content = self.read_file(file_path)
        # content_parts = self.break_file()
        print(content)
        for peer in peers:
            self.send_message(sckt, peer, content)
        print("Sent")


sender = Sender()
p = input()
sender.break_file(p)
# sender.upload_file(p, ('0.0.0.0', 8000))
# sender.send_message(('0.0.0.0', 8000), msg)
