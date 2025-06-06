import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_mongo_collection(collection_name):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client[os.getenv("MONGO_DB_NAME")]
    return db[collection_name]

def get_mongo_client():
    return MongoClient(os.getenv("MONGO_URI"))