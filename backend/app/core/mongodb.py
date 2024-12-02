from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

# MongoDB connection URL
MONGODB_URL = "mongodb://localhost:27017"
DB_NAME = "sports_analysis"

# For async operations
async def get_mongodb():
    client = AsyncIOMotorClient(MONGODB_URL)
    try:
        yield client[DB_NAME]
    finally:
        client.close()

# For sync operations (if needed)
def get_sync_mongodb():
    client = MongoClient(MONGODB_URL)
    return client[DB_NAME]
