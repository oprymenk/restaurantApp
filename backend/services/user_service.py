from backend.db import users_collection
from backend.utils.security import hash_password
from bson import ObjectId
from datetime import datetime

async def create_user(user_data: dict):
    user_data['password'] = hash_password(user_data['password'])
    user_data['created_at'] = datetime.utcnow()
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    user = await users_collection.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def get_user_by_id(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
    return user