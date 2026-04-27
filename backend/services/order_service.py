from backend.db import orders_collection, order_items_collection, menu_items_collection
from bson import ObjectId


async def calculate_total_price(items: list):
    total = 0
    for item in items:
        menu_item = await menu_items_collection.find_one(
            {"_id": ObjectId(item["menu_item_id"])}
        )
        if not menu_item:
            continue
        total += menu_item["price"] * item["quantity"]
    return total

async def create_order(user_id: str, address: str, order_items: list):
    total_price = 0
    order_items_to_insert = []
    #  рахуємо + готуємо items
    for item in order_items:
        menu_item = await menu_items_collection.find_one(
            {"_id": ObjectId(item["menu_item_id"])}
        )
        if not menu_item:
            continue
        price = menu_item["price"]
        quantity = item["quantity"]
        total_price += price * quantity
        order_items_to_insert.append({
            "menu_item_id": ObjectId(item["menu_item_id"]),
            "quantity": quantity,
            "price": price,
            "status": "waiting"
        })
    # створення order
    order = {
        "user_id": ObjectId(user_id),
        "address": address,
        "status": "pending",
        "total_price": total_price
    }
    result = await orders_collection.insert_one(order)
    order_id = result.inserted_id

    for item in order_items_to_insert:
        item["order_id"] = order_id
        await order_items_collection.insert_one(item)
    return str(order_id), total_price


async def get_orders_by_user(user_id: str):
    try:
        user_obj_id = ObjectId(user_id)
    except:
        return []
    orders = await orders_collection.find(
        {"user_id": user_obj_id}
    ).to_list(100)
    for o in orders:
        o["_id"] = str(o["_id"])
        o["user_id"] = str(o["user_id"])
    return orders


async def update_order_status(order_id: str, status: str):
    try:
        obj_id = ObjectId(order_id)
    except:
        return {"error": "Invalid order_id"}
    result = await orders_collection.update_one(
        {"_id": obj_id},
        {"$set": {"status": status}}
    )
    if result.matched_count == 0:
        return {"error": "Order not found"}
    return {"message": f"Order status updated to {status}"}


async def get_kitchen_orders():
    orders = await orders_collection.find(
        {"status": {"$in": ["confirmed", "cooking"]}}
    ).to_list(100)
    for o in orders:
        o["_id"] = str(o["_id"])
        o["user_id"] = str(o["user_id"])
    return orders


async def get_ready_orders():
    orders = await orders_collection.find(
        {"status": "ready"}
    ).to_list(100)
    for o in orders:
        o["_id"] = str(o["_id"])
        o["user_id"] = str(o["user_id"])
    return orders
