"""
User model for demonstration purposes.

This model demonstrates:
- SQLAlchemy 2.0 style with Mapped types
- Async-compatible model definition
- Timestamps using datetime
- Relationships to other models
"""

from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin, PrimaryKeyMixin


class User(Base, TimestampMixin, PrimaryKeyMixin):
    """
    User model representing application users.

    Attributes:
        id: Primary key (from PrimaryKeyMixin)
        username: Unique username
        email: User's email address
        full_name: User's full name (optional)
        is_active: Whether the user account is active
        created_at: Timestamp of user creation (from TimestampMixin)
        updated_at: Timestamp of last update (from TimestampMixin)
        items: Relationship to user's items
    """
    __tablename__ = "users"

    # User information
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    items: Mapped[List["Item"]] = relationship("Item", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"