from fastapi import APIRouter, Depends
from backend.services.order_service import get_kitchen_orders
from backend.utils.dependencies import require_role

router = APIRouter(prefix="/kitchen", tags=["KITCHEN"])

@router.get("/orders")
async def kitchen_orders(
        current_user=Depends(require_role(["kitchen"]))
):
    return await get_kitchen_orders()