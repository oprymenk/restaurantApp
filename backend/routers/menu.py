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

# client
@router.get("/categories")
async def list_categories():
    return await get_categories()

# client
@router.get("/items")
async def list_menu_items(
    category: str | None = Query(None, description="Category ID"),
    sort_by: str | None = Query(
        None,
        enum=["name", "price"],
        description="Sort by field"
    ),
    order: str = Query(
        "asc",
        enum=["asc", "desc"],
        description="Sort order"
    )
):
    return await get_menu_items(category, sort_by, order)

# admin
@router.post("/")
async def add_menu_item(
        item: dict,
        current_user=Depends(require_role(["admin"]))
):
    return await create_menu_item(item)

# admin
@router.put("/{item_id}")
async def edit_menu_item(
        item_id: str,
        item: dict,
        current_user=Depends(require_role(["admin"]))
):
    return await update_menu_item(item_id, item)

# admin
@router.delete("/{item_id}")
async def remove_menu_item(
        item_id: str,
        current_user=Depends(require_role(["admin"]))
):
    return await delete_menu_item(item_id)
