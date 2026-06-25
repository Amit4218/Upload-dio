from src.config.settings import settings
from pymongo import AsyncMongoClient

client = AsyncMongoClient(settings.DATABASE_URL)

def get_collection(collection_name: str):
    """returns the datatbase collection as per the collection_name"""
    db = client["image_uploader"] # database name
    collection = db[collection_name]
    return collection