"""
CRUD operations for Item model.

This module contains async functions to interact with the Item table.
"""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    """
    CRUD operations for Item model.

    Inherits common CRUD operations from CRUDBase and adds item-specific methods.
    """

    async def get_by_owner(
        self,
        db: AsyncSession,
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        """
        Get items belonging to a specific user.

        Args:
            db: Database session
            owner_id: User ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Item objects
        """
        result = await db.execute(
            select(Item)
            .where(Item.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .order_by(Item.created_at.desc())
        )
        return list(result.scalars().all())


# Create a singleton instance
crud_item = CRUDItem(Item)

# Expose functions for backward compatibility
get_item = crud_item.get
get_items = crud_item.get_multi
get_items_by_owner = crud_item.get_by_owner
create_item = crud_item.create
update_item = crud_item.update
delete_item = crud_item.delete
