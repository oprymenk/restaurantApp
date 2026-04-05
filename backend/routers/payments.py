from fastapi import APIRouter, Depends, HTTPException
from backend.services.payment_service import create_payment, get_payment_by_order
from backend.utils.dependencies import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/")
async def new_payment(payment: dict, current_user=Depends(get_current_user)):
    if current_user["role"] != "user":
        raise HTTPException(403, "Only users can pay")
    payment_id = await create_payment(payment["order_id"], payment["amount"], payment["payment_method"], payment["transaction_id"])
    return {"payment_id": payment_id}

@router.get("/order/{order_id}")
async def get_payment(order_id: str, current_user=Depends(get_current_user)):
    payment = await get_payment_by_order(order_id)
    if not payment:
        raise HTTPException(404, "Payment not found")
    return payment