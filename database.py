# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.rename_bot

users = db.users

async def get_user(uid):
    return await users.find_one({"_id": uid})

async def set_user(uid, data):
    await users.update_one(
        {"_id": uid},
        {"$set": data},
        upsert=True
    )

async def add_user(uid):
    await users.update_one(
        {"_id": uid},
        {
            "$setOnInsert": {
                "prefix": "",
                "suffix": "",
                "caption": "",
                "thumb": "",
                "premium": False,
                "banned": False
            }
        },
        upsert=True
    )

async def is_banned(uid):
    user = await get_user(uid)
    return user.get("banned", False) if user else False

async def is_premium(uid):
    user = await get_user(uid)
    return user.get("premium", False) if user else False

async def get_all_users():
    return users.find({})
# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
