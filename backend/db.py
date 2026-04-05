from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client['restaurant_db']


users_collection = db.get_collection("users")
menu_categories_collection = db.get_collection("menu_categories")
menu_items_collection = db.get_collection("menu_items")
orders_collection = db.get_collection("orders")
order_items_collection = db.get_collection("order_items")
payments_collection = db.get_collection("payments")