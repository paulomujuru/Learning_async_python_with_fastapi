"""
Generic CRUD base class to eliminate duplication across CRUD operations.

This module provides a reusable base class for common database operations.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

# Type variables for generic types
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD operations base class.

    This class provides reusable CRUD operations that work with any SQLAlchemy model.
    Inherit from this class and specify the model and schema types.

    Example:
        class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
            pass

    Attributes:
        model: The SQLAlchemy model class
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with a specific model.

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            db: Database session
            id: Record ID to fetch

        Returns:
            Model instance or None if not found
        """
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of model instances
        """
        result = await db.execute(
            select(self.model)
            .offset(skip)
            .limit(limit)
            .order_by(self.model.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
        **extra_fields: Any
    ) -> ModelType:
        """
        Create a new record.

        Args:
            db: Database session
            obj_in: Pydantic schema with creation data
            **extra_fields: Additional fields to set on the model (e.g., owner_id)

        Returns:
            Created model instance
        """
        obj_data = obj_in.model_dump()
        obj_data.update(extra_fields)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        id: int,
        obj_in: UpdateSchemaType
    ) -> Optional[ModelType]:
        """
        Update an existing record.

        Args:
            db: Database session
            id: ID of record to update
            obj_in: Pydantic schema with update data

        Returns:
            Updated model instance or None if not found
        """
        db_obj = await self.get(db, id)
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> bool:
        """
        Delete a record by ID.

        Args:
            db: Database session
            id: ID of record to delete

        Returns:
            True if deleted, False if not found
        """
        db_obj = await self.get(db, id)
        if not db_obj:
            return False

        await db.delete(db_obj)
        await db.flush()
        return True

    async def get_by_field(
        self,
        db: AsyncSession,
        field_name: str,
        field_value: Any
    ) -> Optional[ModelType]:
        """
        Get a single record by a specific field value.

        Args:
            db: Database session
            field_name: Name of the field to filter by
            field_value: Value to match

        Returns:
            Model instance or None if not found
        """
        field = getattr(self.model, field_name)
        result = await db.execute(select(self.model).where(field == field_value))
        return result.scalar_one_or_none()