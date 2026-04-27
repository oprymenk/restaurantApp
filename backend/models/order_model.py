from pydantic import BaseModel, field_validator
from typing import List, Optional

class OrderItemCreate(BaseModel):
    menu_item_id: str
    quantity: int

class OrderCreate(BaseModel):
    address: str
    items: List[OrderItemCreate]

class Order(BaseModel):
    id: str
    user_id: str
    order_type: str = "delivery"
    status: str = "pending"
    address: Optional[str] = None
    total_price: float
    created_at: str
    estimated_time: Optional[int] = 30
    assigned_courier: Optional[str] = None
