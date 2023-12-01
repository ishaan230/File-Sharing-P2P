from central_reg import MongoWrapper

REC_PORT = 8010
DOWN_PORT = 30000


def get_active_peers(recv=False):
    db = MongoWrapper()
    peers = db.get_collection_data("Peer")
    li = []
    for p in peers:
        print(p)
        if p["active"] == "true" or p["active"] == True:
            if recv:
                li.append((p['IP_Address'], REC_PORT))
            else:
                li.append((p['IP_Address'], DOWN_PORT))
    print("active peers: ", li)
    return li
