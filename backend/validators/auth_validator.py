import re
from pydantic import field_validator
from backend.models.auth_model import UserRegister


class UserRegisterValidator(UserRegister):

    @field_validator("name")
    def validate_name(cls, v):
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name too short")
        if not re.match(r"^[A-Za-zА-Яа-яІіЇїЄє\s]+$", v):
            raise ValueError("Name must contain only letters")
        return v

    @field_validator("phone")
    def validate_phone(cls, v):
        if not re.match(r"^\+380\d{9}$", v):
            raise ValueError("Phone must be +380XXXXXXXXX")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password too short")
        if len(v) > 72:
            raise ValueError("Password too long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Need uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Need lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Need number")
        return v
