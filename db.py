import os
import hashlib
import secrets

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGODB_URL")


class DB:
    def __init__(self, uri=URI, db_name="p2p-chat"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.accounts_collection = self.db["accounts"]
        self.online_peers_collection = self.db["online_peers"]

    def is_account_exist(self, username):
        return self.accounts_collection.count_documents({"username": username}) > 0

    def register(self, username, password):
        if self.is_account_exist(username):
            print("Account already exists")
            return False

        salt = secrets.token_hex(16)
        hashed_password = self._hash_password(password, salt)
        account = {"username": username, "password": hashed_password, "salt": salt}
        self.accounts_collection.insert_one(account)
        return True

    def _hash_password(self, password, salt):
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

    def verify_password(self, username, password):
        user = self.accounts_collection.find_one({"username": username})
        if user:
            hashed_password = self._hash_password(password, user["salt"])
            return hashed_password == user["password"]
        else:
            return False

    def is_account_online(self, username):
        return self.online_peers_collection.count_documents({"username": username}) > 0

    def user_login(self, username, ip, port):
        if self.is_account_online(username):
            print("Account is already online")
            return False

        online_peer = {"username": username, "ip": ip, "port": port}
        self.online_peers_collection.insert_one(online_peer)
        return True

    def user_logout(self, username):
        if not self.is_account_online(username):
            print("Account is not online")
            return False

        self.online_peers_collection.delete_one({"username": username})

    def get_peer_ip_port(self, username):
        res = self.online_peers_collection.find_one({"username": username})
        if res:
            return (res["ip"], res["port"])
        else:
            return None

    def drop_all_records(self):
        self.accounts_collection.delete_many({})
        self.online_peers_collection.delete_many({})


# Dummy Code to Test Database
# if __name__ == "__main__":
#     db = DB()

#     # db.register("Ayman", "False")
#     if db.verify_password("Ayman", "False"):
#         print("Password is correct")
