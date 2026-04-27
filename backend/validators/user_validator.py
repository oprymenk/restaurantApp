import re

def validate_name(v: str):
    v = v.strip()
    if len(v) < 2:
        raise ValueError("Name too short")
    if len(v) > 50:
        raise ValueError("Name too long")
    if not re.match(r"^[A-Za-zА-Яа-яІіЇїЄє\s]+$", v):
        raise ValueError("Name must contain only letters")
    return v

def validate_phone(v: str):
    v = v.strip()
    if not re.match(r"^\+380\d{9}$", v):
        raise ValueError("Phone must be in format +380XXXXXXXXX")
    return v

def validate_role(v: str):
    allowed_roles = ["user", "admin", "manager", "courier", "kitchen"]
    if v not in allowed_roles:
        raise ValueError(f"Role must be one of {allowed_roles}")
    return v

def validate_password(v: str):
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters")
    if len(v) > 72:
        raise ValueError("Password too long (max 72 chars)")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Must contain uppercase letter")
    if not re.search(r"[a-z]", v):
        raise ValueError("Must contain lowercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Must contain number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("Must contain special character")
    return v
