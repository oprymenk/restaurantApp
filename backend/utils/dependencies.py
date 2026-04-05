from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from backend.db import users_collection
from backend.utils.security import decode_access_token
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await users_collection.find_one({"_id": ObjectId(payload.get("user_id"))})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["_id"] = str(user["_id"])
    return user

def require_role(roles: list):
    async def role_checker(current_user=Depends(get_current_user)):

        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Allowed roles: {roles}"
            )

        return current_user

    return role_checker