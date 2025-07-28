import certifi
from pymongo import AsyncMongoClient

from .utils import get_secret

MONGO_URI = get_secret("MONGO_URI", "")


# Send a ping to confirm a successful connection
async def database_connect() -> None:
    try:
        client = AsyncMongoClient(MONGO_URI, tlsCAFile=certifi.where())
        await client.aconnect()
        await client.admin.command("ping")
        print("Successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
