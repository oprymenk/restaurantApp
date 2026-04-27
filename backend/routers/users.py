from fastapi import APIRouter, Depends, HTTPException
from backend.services.user_service import (
    get_user_by_id,
    get_user_by_email,
    create_user,
    get_all_users,
    update_user,
    delete_user
)
from backend.models.user_model import UserCreate
from backend.utils.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def read_me(current_user=Depends(get_current_user)):
    return current_user


# admin
@router.get("/")
async def all_users(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Not enough permissions")

    return await get_all_users()

@router.get("/{user_id}")
async def get_user(user_id: str, current_user=Depends(get_current_user)):

    if current_user["role"] not in ["admin", "manager"] and current_user["_id"] != user_id:
        raise HTTPException(403, "Not enough permissions")
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.post("/")
async def create_new_user(
    user: UserCreate,
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Not enough permissions")
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(400, "Email already exists")
    user_id = await create_user(user.dict())
    return {"user_id": user_id}

@router.put("/{user_id}")
async def update_user_route(
    user_id: str,
    data: dict,
    current_user=Depends(get_current_user)
):
    # user може редагувати тільки себе
    if current_user["role"] != "admin" and current_user["_id"] != user_id:
        raise HTTPException(403, "Not enough permissions")
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    updated = await update_user(user_id, data)
    if updated == 0:
        return {"message": "No changes applied"}
    return {"message": "User updated"}

@router.delete("/{user_id}")
async def delete_user_route(
    user_id: str,
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(403, "Not enough permissions")
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    await delete_user(user_id)
    return {"message": "User deleted"}
