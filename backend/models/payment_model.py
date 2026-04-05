from pydantic import BaseModel, Field

class Payment(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    order_id: str
    amount: float
    payment_method: str
    status: str = "paid"
    transaction_id: str