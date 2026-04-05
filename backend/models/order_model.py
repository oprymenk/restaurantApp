from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Order(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    user_id: str
    order_type: str = "delivery"
    status: str = "pending"
    address: Optional[str]
    total_price: float
    created_at: datetime
    estimated_time: Optional[int]
    assigned_courier: Optional[str]

class OrderItem(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    order_id: str
    menu_item_id: str
    quantity: int
    price: float
    status: str = "waiting"