import pymongo
from dotenv import load_dotenv
import os


class MongoWrapper:
    # db_name: File, FileParts, Peers
    def __init__(self):
        load_dotenv()
        print(os.environ.get("DB_URI"))
        db_uri = os.environ.get("DB_URI")
        # db_uri = ""
        self.mongo_cli = pymongo.MongoClient(db_uri)
        self.collections = ["File", "Peer", "Part"]
        self.set_databases()
        self.set_collection()

    def set_databases(self):
        self.primary_db = self.mongo_cli["SeDB"]

    def set_collection(self):
        collection_list = self.primary_db.list_collection_names()
        for col in self.collections:
            if col not in collection_list:
                print(f"Created {col}")
                self.primary_db[col]

    def get_collection_data(self, collection):
        return self.primary_db[collection].find({})

    def add_data_to_collection(self, collection_name, data):
        try:
            data = self.primary_db[collection_name].insert_one(data)
            return str(data.inserted_id)
        except Exception:
            return None
        
    # https://www.w3schools.com/python/python_mongodb_update.asp
    def update_data(self, collection_name, data, updated_data) -> bool:
        dt = {"$set": updated_data}
        try:
            self.primary_db[collection_name].update_one(data, dt)
            return True
        except Exception:
            return False
        
    def get_peer_data(self, user_id):
        try:
            peer = self.primary_db["Peer"].find_one({ "user_id": user_id})
            return peer
        except Exception as e:
            return e
        
    def get_file_data(self, file_uid):
        try:
            file = self.primary_db["File"].find_one({ "file_uid": file_uid})
            return file
        except Exception as e:
            return e
        
    def get_parts_for_file(self, file_uid):
        try:
            cursor = self.primary_db["Part"].find({"file_uid": file_uid})
            return cursor
        except Exception as e:
            return e
        
    def get_user_ip(self, user_id):
        try:
            peer = self.primary_db['Peer'].find_one({'user_id': user_id})
            return peer['user_ip']
        except Exception as e:
            return e    


# mn = MongoWrapper()
#
# mn.add_data_to_collection("File", {"name": "Test file", "size": 50})
#
# data = mn.get_collection_data("File")
#
# for a in data:
#     print(a)
#
