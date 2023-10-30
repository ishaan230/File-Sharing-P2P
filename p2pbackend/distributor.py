import socket
from file_utils import break_file
import os
import json

'''
Provide addresses in tuple format
Handshaked peers should only be allowed
'''


class Sender:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip_addr = socket.gethostbyname(self.hostname)
        self.port = 65432
        self.alt_port = 54321
        self.CHUNK_SIZE = 1024

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
        return break_file(file_path, self.CHUNK_SIZE)

    def populate_peers(self, peers, parts):
        ctr = [i for i in range(0, len(parts))]
        if len(peers) == len(parts):
            return zip(ctr, peers, parts)
        elif len(peers) > len(parts):
            return zip(ctr, peers[0:len(parts)], parts)
        else:
            new_peers = peers
            extra_req = len(parts) - len(peers)
            print(extra_req)
            i = 0
            iter = 0
            while i < extra_req:
                print(iter)
                if iter >= len(peers):
                    iter = 0
                new_peers.append(peers[iter])
                iter += 1
                i += 1
            return zip(ctr, new_peers, parts)

    def upload_file(self, file_path, peers):
        sckt = self.setup_listener()
        parts = self.break_file(file_path)
        file_type = os.path.splitext(file_path)
        for ctr, peer, part in self.populate_peers(peers, parts):
            print(peer)
            meta = {"file_name": f'{ctr}.part', "extension": file_type, "content": part, "offset": ctr, "length": len(parts), "original_size": len(parts)*self.CHUNK_SIZE}
            json_meta = json.dumps(meta)
            print(json_meta)
            self.send_message(sckt, peer, json_meta)
        print("Sent")


if __name__ == "__main__":
    sender = Sender()
    peers = ['0.0.0.0:8000']
    sender.upload_file('o.jpg', peers)
