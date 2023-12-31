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
            peer = self.primary_db["Peer"].find_one({ "User_id": user_id})
            return peer
        except Exception as e:
            return e
        
    def get_part_data(self, file_uid, offset):
        try:
            part = self.primary_db["Part"].find_one({ "file_uid": file_uid, "offset": offset})
            return part
        except Exception as e:
            return e
        
    def get_file_data(self, hash):
        try:
            file = self.primary_db["File"].find_one({ "hash": hash})
            return file
        except Exception as e:
            return e
        
    def get_part_seeds(self, file_uid, offset):
        try:
            part = self.primary_db["Part"].find_one({ "file_uid": file_uid, "offset": offset})
            return part['users']
        except Exception as e:
            return e
        
    def update_seeders_post_download(self, file_uid, offset):
        try:
            users = self.get_part_seeds(file_uid, offset)
            users += [os.environ['USER_ID']]
            self.update_data('Part', { 'file_uid': file_uid, 'offset': offset }, {'users': users})
        except Exception as e:
            return e
        
    def get_parts_for_file(self, file_uid):
        try:
            cursor = self.primary_db["Part"].find({"file_id": file_uid})
            return cursor
        except Exception as e:
            return e
        
    def get_user_ip(self, user_id):
        try:
            peer = self.primary_db['Peer'].find_one({'User_id': user_id})
            return peer['IP_Address']
        except Exception as e:
            return e    
        
    def delete_part(self, file_uid, offset):
        try:
            result = self.primary_db["Part"].delete_one({'file_uid': file_uid, 'offset': offset})
            return result
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
