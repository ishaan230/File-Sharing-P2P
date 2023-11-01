import pymongo


class MongoWrapper:
    # db_name: File, FileParts, Peers
    def __init__(self):
        db_uri = "mongodb+srv://seproj:seproj2023@cluster0.pw1hy3v.mongodb.net/?retryWrites=true&w=majority"
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


# mn = MongoWrapper()
#
# mn.add_data_to_collection("File", {"name": "Test file", "size": 50})
#
# data = mn.get_collection_data("File")
#
# for a in data:
#     print(a)
#
