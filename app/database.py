import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DB")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)

db = client[MONGODB_DATABASE]

# Define collections for easy access
notes_collection = db.notes
users_collection = db.users


# Create unique indexes
async def create_indexes():
    await users_collection.create_index("email",unique=True)
    await users_collection.create_index("username",unique=True)
    await notes_collection.create_index("user_id")
    await notes_collection.create_index("title", unique=True)
    
# Call this function during application startup
async def startup_db_client():
    await create_indexes()
