"""
API routes for Item operations.

This module demonstrates:
- CRUD operations with async database
- Relationship handling (items belong to users)
- Query parameters for filtering
"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import raise_not_found
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.crud import item as crud_item
from app.crud import user as crud_user

router = APIRouter()


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    owner_id: int = Query(..., description="ID of the user who owns this item"),
    db: AsyncSession = Depends(get_db)
) -> ItemResponse:
    """
    Create a new item.

    Args:
        item: Item data from request body
        owner_id: ID of the user who owns this item (query parameter)
        db: Database session (injected)

    Returns:
        Created item data

    Raises:
        HTTPException: 404 if owner doesn't exist
    """
    # Verify that the owner exists
    owner = await crud_user.get_user(db, id=owner_id)
    if not owner:
        raise_not_found("Owner", owner_id)

    return await crud_item.create_item(db=db, obj_in=item, owner_id=owner_id)


@router.get("/items", response_model=List[ItemResponse])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    owner_id: int = Query(None, description="Filter items by owner ID"),
    db: AsyncSession = Depends(get_db)
) -> List[ItemResponse]:
    """
    Retrieve a list of items with optional filtering.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100, max: 100)
        owner_id: Optional filter by owner ID
        db: Database session (injected)

    Returns:
        List of items
    """
    if owner_id is not None:
        items = await crud_item.get_items_by_owner(
            db, owner_id=owner_id, skip=skip, limit=min(limit, 100)
        )
    else:
        items = await crud_item.get_items(db, skip=skip, limit=min(limit, 100))
    return items


@router.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
) -> ItemResponse:
    """
    Get a specific item by ID.

    Args:
        item_id: Item ID
        db: Database session (injected)

    Returns:
        Item data

    Raises:
        HTTPException: 404 if item not found
    """
    db_item = await crud_item.get_item(db, id=item_id)
    if db_item is None:
        raise_not_found("Item", item_id)
    return db_item


@router.patch("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_db)
) -> ItemResponse:
    """
    Update an item's information.

    Args:
        item_id: Item ID
        item: Updated item data (partial updates allowed)
        db: Database session (injected)

    Returns:
        Updated item data

    Raises:
        HTTPException: 404 if item not found
    """
    db_item = await crud_item.update_item(db, id=item_id, obj_in=item)
    if db_item is None:
        raise_not_found("Item", item_id)
    return db_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete an item.

    Args:
        item_id: Item ID
        db: Database session (injected)

    Raises:
        HTTPException: 404 if item not found
    """
    success = await crud_item.delete_item(db, id=item_id)
    if not success:
        raise_not_found("Item", item_id)