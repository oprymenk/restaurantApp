from fastapi import FastAPI
from backend.routers import auth, users, menu, orders, payments, courier, kitchen

app = FastAPI(title="Restaurant Delivery API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(courier.router)
app.include_router(kitchen.router)
