from userdetails import get_ip
import socket
import asyncio
import base64
import os
import json
import time

PORT = 8010


async def save_data(client):
    loop = asyncio.get_event_loop()
    # request = b""
    request = await loop.sock_recv(client, 1024*1024)
    # print("Data received: ", request)
    req = request.decode('utf-8')
    # try:
    st = json.loads(req)
    # except json.JSONDecodeError:
    #     print("JSON-> ", req)
    #     exit()
    # print("VAVVV", st)
    # Extract bin string
    try:
        os.mkdir(f'/home/{os.getlogin()}/.localran/')
    except FileExistsError:
        print("Exists...")

    file_content = st['content']
    file_content = base64.b64decode(file_content)
    # print("File content: ", file_content)
    try:
        os.mkdir(f'/home/{os.getlogin()}/.localran/{st["original_name"]}-{st["timestamp"]}')
    except FileExistsError:
        print("Exists")
    with open(f'/home/{os.getlogin()}/.localran/{st["original_name"]}-{st["timestamp"]}/{st["original_name"] + st["part_file_name"] + st["extension"]}', "wb") as file:
        print("WRITING")
        ac = file_content
        file.write(ac)
    print("RECEIVED")
    client.close()


async def setup_recieve_data():
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    # print("Upload receive socket..", sck)
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("IP-> ", get_ip(), PORT)
    sck.bind((get_ip(), PORT))
    # print("BINDING DONE")
    sck.setblocking(False)
    sck.listen(8)
    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(sck)
        print("Listening------")
        loop.create_task(save_data(client))
        # data = sck.recv(1024)
        # print(data)
