from fastapi import APIRouter, Depends
from backend.services.order_service import get_ready_orders
from backend.utils.dependencies import require_role

router = APIRouter(prefix="/courier", tags=["COURIER"])

@router.get("/available-orders")
async def ready_orders(
        current_user=Depends(require_role(["courier"]))
):
    return await get_ready_orders()