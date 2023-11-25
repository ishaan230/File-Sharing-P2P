from userdetails import get_ip
import socket
import asyncio
import random
import json

PORT = 8010


async def save_data(client):
    loop = asyncio.get_event_loop()
    # request = b""
    request = await loop.sock_recv(client, 1024*1024)
    print("VALL", request)
    req = request.decode('utf-8')
    st = json.loads(req)
    print("VAVVV", st)
    with open(f'/home/akshat/{st["original_name"] + st["part_file_name"] + st["extension"]}', "w") as file:
        print("WRITING")
        ac = b'' + st['content']
        file.write(ac)
    # while request != b'\0' or len(request) != 0:
    #     print("VALLL", request)
    #     # with open('/home/akshat/Akshat.part', "wb") as file:
    #     #     print("WRITING")
    #     #     file.write(request)
    #     print(client)
    #     request = (await loop.sock_recv(client, 1024*1024))
    #     print(request)
        # await loop.sock_send(client, "True".encode('utf-8'))
    print("RECEIVED")
    client.close()


async def setup_recieve_data():
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print(sck)
    sck.bind((get_ip(), PORT))
    print("BINDING DONE")
    # sck.setblocking(False)
    sck.listen(8)
    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(sck)
        loop.create_task(save_data(client))
        data = sck.recv(1024)
        print(data)
