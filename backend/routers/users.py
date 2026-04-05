from fastapi import APIRouter, Depends, HTTPException
from backend.services.user_service import get_user_by_id, get_user_by_email, create_user
from backend.models.user_model import UserCreate
from backend.utils.dependencies import get_current_user
from backend.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def read_me(current_user=Depends(get_current_user)):
    return current_user

# MANAGER / ADMIN - отримати користувача по id
@router.get("/{user_id}")
async def get_user(user_id: str, current_user=Depends(get_current_user)):
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(403, "Not enough permissions")
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

# ADMIN - створити користувача
@router.post("/")
async def create_new_user(user: UserCreate, current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Not enough permissions")
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(400, "Email already exists")
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_id = await create_user(user_dict)
    return {"user_id": user_id}
