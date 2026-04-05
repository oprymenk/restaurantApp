from pydantic import BaseModel, Field
from typing import Optional

class MenuCategory(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    description: Optional[str]

class MenuItem(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    name: str
    description: Optional[str]
    price: float
    category_id: str
    image: Optional[str]
    available: bool = True