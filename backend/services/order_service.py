from backend.db import orders_collection, order_items_collection
from bson import ObjectId
from datetime import datetime


# CLIENT - створення замовлення
async def create_order(user_id: str, address: str, order_items: list, total_price: float):

    order = {
        "user_id": ObjectId(user_id),
        "order_type": "delivery",
        "status": "pending",
        "address": address,
        "total_price": total_price,
        "created_at": datetime.utcnow(),
        "estimated_time": 30,
        "assigned_courier": None
    }

    result = await orders_collection.insert_one(order)
    order_id = result.inserted_id

    # створення order_items
    for item in order_items:
        await order_items_collection.insert_one({
            "order_id": order_id,
            "menu_item_id": ObjectId(item["menu_item_id"]),
            "quantity": item["quantity"],
            "price": item["price"],
            "status": "waiting"
        })

    return str(order_id)


# CLIENT - отримати свої замовлення
async def get_orders_by_user(user_id: str):

    orders = await orders_collection.find(
        {"user_id": ObjectId(user_id)}
    ).to_list(100)

    for o in orders:
        o["_id"] = str(o["_id"])
        o["user_id"] = str(o["user_id"])

    return orders


# MANAGER / KITCHEN / COURIER - змінити статус замовлення
async def update_order_status(order_id: str, status: str):

    result = await orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": status}}
    )

    if result.matched_count == 0:
        return {"error": "Order not found"}

    return {"message": f"Order status updated to {status}"}


# KITCHEN - замовлення для кухні
async def get_kitchen_orders():

    orders = await orders_collection.find(
        {"status": {"$in": ["confirmed", "cooking"]}}
    ).to_list(100)

    for o in orders:
        o["_id"] = str(o["_id"])
        o["user_id"] = str(o["user_id"])

    return orders


# COURIER - готові замовлення
async def get_ready_orders():

    orders = await orders_collection.find(
        {"status": "ready"}
    ).to_list(100)

    for o in orders:
        o["_id"] = str(o["_id"])
        o["user_id"] = str(o["user_id"])

    return orders