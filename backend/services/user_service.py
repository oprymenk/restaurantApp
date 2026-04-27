from backend.db import users_collection
from backend.utils.security import hash_password
from bson import ObjectId
from datetime import datetime

async def create_user(user_data: dict):
    user_data["password"] = hash_password(user_data["password"])
    user_data["created_at"] = datetime.utcnow()
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)

async def get_user_by_email(email: str):
    user = await users_collection.find_one({"email": email})
    if user:
        user["_id"] = str(user["_id"])
    return user

async def get_user_by_id(user_id: str):
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        return None
    if user:
        user["_id"] = str(user["_id"])
    return user

async def get_all_users():
    users = await users_collection.find().to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])
    return users


async def update_user(user_id: str, data: dict):
    try:
        obj_id = ObjectId(user_id)
    except:
        return None
    # якщо змінюється пароль - хешуємо
    if "password" in data:
        data["password"] = hash_password(data["password"])
    result = await users_collection.update_one(
        {"_id": obj_id},
        {"$set": data}
    )
    return result.modified_count


async def delete_user(user_id: str):
    try:
        obj_id = ObjectId(user_id)
    except:
        return None
    result = await users_collection.delete_one({"_id": obj_id})
    return result.deleted_count
