"""
Pydantic schemas for Item model.

These schemas are used for:
- Request validation (Create, Update)
- Response serialization (Response)
"""

from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.base import BaseResponseSchema


class ItemBase(BaseModel):
    """Base Item schema with common attributes."""
    title: str = Field(..., min_length=1, max_length=100, description="Item title")
    description: Optional[str] = Field(None, description="Item description")
    is_published: bool = Field(default=False, description="Whether the item is published")


class ItemCreate(ItemBase):
    """
    Schema for creating a new item.

    Used in POST requests to create items.
    Owner is determined from authentication context.
    """
    pass


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing item.

    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_published: Optional[bool] = None


class ItemResponse(ItemBase, BaseResponseSchema):
    """
    Schema for item responses.

    Includes all fields that should be returned to clients.
    Inherits id, created_at, updated_at from BaseResponseSchema.
    """
    owner_id: int