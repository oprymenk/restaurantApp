from backend.db import menu_categories_collection, menu_items_collection
from bson import ObjectId

async def get_categories():
    categories = await menu_categories_collection.find().to_list(100)
    for c in categories:
        c["_id"] = str(c["_id"])
    return categories

async def get_menu_items(category_id: str = None, sort_by: str = None, order: str = "asc"):
    query = {}
    if category_id:
        query["category_id"] = ObjectId(category_id)
    cursor = menu_items_collection.find(query)

    # сортування
    if sort_by:
        direction = 1 if order == "asc" else -1
        cursor = cursor.sort(sort_by, direction)

    items = await cursor.to_list(100)

    for i in items:
        i["_id"] = str(i["_id"])
        i["category_id"] = str(i["category_id"])

    return items


# ADMIN - створити нову страву
async def create_menu_item(item: dict):

    item["category_id"] = ObjectId(item["category_id"])

    result = await menu_items_collection.insert_one(item)

    return {
        "message": "Menu item created",
        "item_id": str(result.inserted_id)
    }


# ADMIN - редагувати страву
async def update_menu_item(item_id: str, item: dict):

    if "category_id" in item:
        item["category_id"] = ObjectId(item["category_id"])

    result = await menu_items_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item}
    )

    if result.matched_count == 0:
        return {"error": "Item not found"}

    return {"message": "Menu item updated"}


# ADMIN - видалити страву
async def delete_menu_item(item_id: str):

    result = await menu_items_collection.delete_one(
        {"_id": ObjectId(item_id)}
    )

    if result.deleted_count == 0:
        return {"error": "Item not found"}

    return {"message": "Menu item deleted"}