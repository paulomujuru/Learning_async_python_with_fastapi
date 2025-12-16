"""
Pydantic schemas for User model.

These schemas are used for:
- Request validation (Create, Update)
- Response serialization (Response)
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseResponseSchema


class UserBase(BaseModel):
    """Base User schema with common attributes."""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Used in POST requests to create users.
    """
    is_active: bool = Field(default=True, description="Whether the user account is active")


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.

    All fields are optional to allow partial updates.
    """
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class UserResponse(UserBase, BaseResponseSchema):
    """
    Schema for user responses.

    Includes all fields that should be returned to clients.
    Inherits id, created_at, updated_at from BaseResponseSchema.
    """
    is_active: bool