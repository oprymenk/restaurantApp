from fastapi import APIRouter, Depends, HTTPException, Query
from backend.services.menu_service import (
    get_categories,
    get_menu_items,
    create_menu_item,
    update_menu_item,
    delete_menu_item
)
from backend.utils.dependencies import require_role

router = APIRouter(prefix="/menu", tags=["MENU"])

# CLIENT
@router.get("/categories")
async def list_categories():
    return await get_categories()


# CLIENT
@router.get("/items")
async def list_menu_items(
        category: str | None = None,
        sort_by: str | None = Query(None, enum=["name", "price"]),
        order: str = Query("asc", enum=["asc", "desc"])
):
    return await get_menu_items(category, sort_by, order)


# ADMIN
@router.post("/")
async def add_menu_item(
        item: dict,
        current_user=Depends(require_role(["admin"]))
):
    return await create_menu_item(item)


# ADMIN
@router.put("/{item_id}")
async def edit_menu_item(
        item_id: str,
        item: dict,
        current_user=Depends(require_role(["admin"]))
):
    return await update_menu_item(item_id, item)


# ADMIN
@router.delete("/{item_id}")
async def remove_menu_item(
        item_id: str,
        current_user=Depends(require_role(["admin"]))
):
    return await delete_menu_item(item_id)