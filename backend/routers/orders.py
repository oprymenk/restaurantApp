from fastapi import APIRouter, Depends, HTTPException
from backend.services.order_service import *
from backend.utils.dependencies import require_role

router = APIRouter(prefix="/orders", tags=["ORDERS"])


# CLIENT - створення замовлення
@router.post("/")
async def create(
        order: dict,
        current_user=Depends(require_role(["user"]))
):
    order_id = await create_order(
        current_user["_id"],
        order["address"],
        order["items"],
        order["total_price"]
    )
    return {"order_id": order_id}


# CLIENT - перегляд своїх замовлень
@router.get("/my")
async def my_orders(
        current_user=Depends(require_role(["user"]))
):
    return await get_orders_by_user(current_user["_id"])


#  MANAGER - підтвердити
@router.patch("/{order_id}/confirm")
async def confirm_order(
        order_id: str,
        current_user=Depends(require_role(["manager"]))
):
    return await update_order_status(order_id, "confirmed")


# MANAGER - відправити на кухню
@router.patch("/{order_id}/send-to-kitchen")
async def send_to_kitchen(
        order_id: str,
        current_user=Depends(require_role(["manager"]))
):
    return await update_order_status(order_id, "cooking")


# KITCHEN - змінити статус cooking - ready
@router.patch("/{order_id}/ready")
async def ready_order(
        order_id: str,
        current_user=Depends(require_role(["kitchen"]))
):
    return await update_order_status(order_id, "ready")


# COURIER - взяти замовлення
@router.patch("/{order_id}/take")
async def take_order(
        order_id: str,
        current_user=Depends(require_role(["courier"]))
):
    return await update_order_status(order_id, "delivering")


# COURIER - доставлено
@router.patch("/{order_id}/delivered")
async def delivered(
        order_id: str,
        current_user=Depends(require_role(["courier"]))
):
    return await update_order_status(order_id, "delivered")


# MANAGER - завершити
@router.patch("/{order_id}/complete")
async def complete(
        order_id: str,
        current_user=Depends(require_role(["manager"]))
):
    return await update_order_status(order_id, "completed")