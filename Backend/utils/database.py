import os

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Database:
    def __init__(self):
        self.client = None
        self.db = None
        try:
            self.client = MongoClient(
                os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
            )
            db_name = os.environ.get("MONGO_DB_NAME", "etoaudiobook")
            self.db = self.client[db_name]
            self.client.admin.command("ping")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        if self.db is not None:
            return self.db[collection_name]
        return None


db = Database()
