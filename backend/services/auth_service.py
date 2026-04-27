from backend.db import users_collection
from backend.utils.security import hash_password, verify_password


async def register_user(user_dict: dict):
    user_dict["password"] = hash_password(user_dict["password"])
    result = await users_collection.insert_one(user_dict)
    return str(result.inserted_id)


async def get_user_by_email(email: str):
    return await users_collection.find_one({"email": email})
