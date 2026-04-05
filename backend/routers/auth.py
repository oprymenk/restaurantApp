from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend.db import users_collection
from backend.utils.security import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: str  # user, manager, admin, kitchen, courier, payment_system
    password: str

@router.post("/register")
async def register(user: UserRegister):
    try:
        existing = await users_collection.find_one({"email": user.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_dict = user.dict()
        user_dict["password"] = hash_password(user.password)
        user_dict["created_at"] = "2026-04-02"

        result = await users_collection.insert_one(user_dict)
        return {"user_id": str(result.inserted_id)}

    except Exception as e:
        print("Register error:", e)
        raise HTTPException(status_code=500, detail=str(e))