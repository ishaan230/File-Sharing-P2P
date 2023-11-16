from central_reg import MongoWrapper

def get_active_peers():
    db = MongoWrapper()
    peers = db.get_collection_data("Peer")
    li = []
    for p in peers:
        li.append((p['IP_Address'], 8001))
    return li
