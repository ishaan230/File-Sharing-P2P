import socket
import time
from file_utils import break_file
import os
import json
import hashlib
import base64

from central_reg import MongoWrapper
from userdetails import get_ip

'''
Provide addresses in tuple format
'''


class Sender:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.ip_addr = get_ip()
        self.port = 65432
        self.alt_port = 54321
        self.CHUNK_SIZE = 65530
        self.db_engine = MongoWrapper()

    def setup_listener(self):
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sckt.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
        print("SEOCKER", sckt)
        return sckt

    def send_message(self, sckt, client_addr, content):
        if sckt:
            print(client_addr)
            sckt.connect(client_addr)
            # print("SENDING->", content)
            total_sent = 0
            while total_sent < len(content):
                sent = sckt.send(content[total_sent:])
                if sent == 0:
                    raise RuntimeError("Socket Connection broken")
                total_sent += sent
                print("SENT ", total_sent)
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
            i = 0
            iter = 0
            while i < extra_req:
                if iter >= len(peers):
                    iter = 0
                new_peers.append(peers[iter])
                iter += 1
                i += 1
            return zip(ctr, new_peers, parts)

    def upload_file(self, file_path, peers):
        parts = self.break_file(file_path)
        file_info = os.path.splitext(file_path)
        filename = file_info[0]
        if filename.__contains__('/'):
            filename = filename[filename.rindex('/')+1:]
        orig_file = filename
        filename = hashlib.md5(filename.encode('utf-8')).hexdigest()
        file_meta = {"name": orig_file+file_info[1], "hash": filename, "size": len(parts) * self.CHUNK_SIZE, "type": file_info[1]}
        file_id = self.db_engine.add_data_to_collection("File", file_meta)
        print("File Id: ", file_id)
        timestamp = time.time()
        for ctr, peer, part in self.populate_peers(peers, parts):
            sckt = self.setup_listener()
            print("sending for peer ", peer)
            meta = {"part_file_name": f'{ctr}.part',
                    "original_name": orig_file,
                    "file_id": file_id,
                    "extension": file_info[1], "content": part,
                    "offset": ctr, "length": len(parts),
                    "user_mac": "TBD",
                    "timestamp": timestamp,
                    "original_size": len(parts)*self.CHUNK_SIZE}
            json_meta = json.dumps(meta)
            self.send_message(sckt, peer, json_meta.encode('utf-8'))
            sckt.close()
            print("Sent for ", peer)
            meta.pop("content")
            print("Udating registry")
            self.db_engine.add_data_to_collection('Part', meta)
            print("Updated Registry")


# if __name__ == "__main__":
#     sender = Sender()
#     peers = ['0.0.0.0:8000']
#     sender.upload_file('/home/akshat/clg/se_project/File-Sharing-P2P/p2pbackend/o.jpg', peers)
