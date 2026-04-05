from backend.db import payments_collection
from bson import ObjectId
from datetime import datetime

async def create_payment(order_id: str, amount: float, method: str, transaction_id: str):
    payment = {
        "order_id": ObjectId(order_id),
        "amount": amount,
        "payment_method": method,
        "status": "paid",
        "transaction_id": transaction_id,
        "created_at": datetime.utcnow()
    }
    result = await payments_collection.insert_one(payment)
    return str(result.inserted_id)

async def get_payment_by_order(order_id: str):
    payment = await payments_collection.find_one({"order_id": ObjectId(order_id)})
    if payment:
        payment["_id"] = str(payment["_id"])
        payment["order_id"] = str(payment["order_id"])
    return payment