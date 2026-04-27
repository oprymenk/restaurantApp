from fastapi import APIRouter, Depends
from backend.services.order_service import *
from backend.models.order_model import OrderCreate
from backend.utils.dependencies import get_current_user, require_role

router = APIRouter(prefix="/orders", tags=["ORDERS"])


# create order
@router.post("/")
async def create(
    order: OrderCreate,
    current_user=Depends(get_current_user)
):
    order_id, total = await create_order(
        current_user["_id"],
        order.address,
        [item.dict() for item in order.items]
    )
    return {
        "order_id": order_id,
        "total_price": total
    }

# my orders
@router.get("/my")
async def my_orders(
    current_user=Depends(get_current_user)
):
    return await get_orders_by_user(current_user["_id"])

# manager
@router.patch("/{order_id}/confirm")
async def confirm_order(order_id: str, current_user=Depends(require_role(["manager"]))):
    return await update_order_status(order_id, "confirmed")

@router.patch("/{order_id}/send-to-kitchen")
async def send_to_kitchen(order_id: str, current_user=Depends(require_role(["manager"]))):
    return await update_order_status(order_id, "cooking")

@router.patch("/{order_id}/complete")
async def complete(order_id: str, current_user=Depends(require_role(["manager"]))):
    return await update_order_status(order_id, "completed")

# kitchen
@router.patch("/{order_id}/ready")
async def ready_order(order_id: str, current_user=Depends(require_role(["kitchen"]))):
    return await update_order_status(order_id, "ready")

# courier
@router.patch("/{order_id}/take")
async def take_order(order_id: str, current_user=Depends(require_role(["courier"]))):
    return await update_order_status(order_id, "delivering")

@router.patch("/{order_id}/delivered")
async def delivered(order_id: str, current_user=Depends(require_role(["courier"]))):
    return await update_order_status(order_id, "delivered")
