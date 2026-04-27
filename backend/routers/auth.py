from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.validators.auth_validator import UserRegisterValidator
from backend.services.auth_service import register_user, get_user_by_email
from backend.utils.security import verify_password, create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserRegisterValidator):
    existing = await get_user_by_email(user.email)
    if existing:
        raise HTTPException(400, "Email already exists")
    user_id = await register_user(user.dict())
    return {"user_id": user_id}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(401, "Invalid credentials")
    access_token = create_access_token(
        {"user_id": str(user["_id"]), "role": user["role"]}
    )
    refresh_token = create_refresh_token(
        {"user_id": str(user["_id"])}
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
