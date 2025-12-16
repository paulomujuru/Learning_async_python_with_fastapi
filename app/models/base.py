"""
Base model mixins for common patterns.

This module provides reusable mixins for SQLAlchemy models to reduce duplication.
"""

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class TimestampMixin:
    """
    Mixin that adds created_at and updated_at timestamp fields.

    Use this mixin in any model that needs automatic timestamp tracking.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


class PrimaryKeyMixin:
    """
    Mixin that adds a standard integer primary key with index.

    Use this mixin in any model that needs a standard auto-incrementing ID.
    """
    id: Mapped[int] = mapped_column(primary_key=True, index=True)