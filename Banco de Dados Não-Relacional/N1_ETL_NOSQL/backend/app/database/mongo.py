from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from app.config import MONGODB_URI, MONGODB_DB

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    return _client


def get_db() -> Database:
    return get_client()[MONGODB_DB]


def ping_db() -> bool:
    try:
        get_client().admin.command("ping")
        return True
    except ConnectionFailure:
        return False
