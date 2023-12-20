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
        salt = secrets.token_hex(16)
        hashed_password = self._hash_password(password, salt)
        account = {"username": username, "password": hashed_password, "salt": salt}
        self.accounts_collection.insert_one(account)

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
        online_peer = {"username": username, "ip": ip, "port": port}
        self.online_peers_collection.insert_one(online_peer)

    def user_logout(self, username):
        self.online_peers_collection.delete_one({"username": username})

    def get_peer_ip_port(self, username):
        res = self.online_peers_collection.find_one({"username": username})
        if res:
            return (res["ip"], res["port"])
        else:
            return None

