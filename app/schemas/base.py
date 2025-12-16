"""
Base Pydantic schemas for common patterns.

This module provides reusable base schemas to reduce duplication across schema definitions.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TimestampSchema(BaseModel):
    """
    Schema mixin that adds timestamp fields.

    Use this when you need to include created_at and updated_at in responses.
    """
    created_at: datetime
    updated_at: datetime


class BaseResponseSchema(BaseModel):
    """
    Base response schema with id and timestamps.

    Extend this for any resource that has an ID and timestamp fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)