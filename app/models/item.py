"""
Item model for demonstration purposes.

This model demonstrates:
- Foreign key relationships
- SQLAlchemy 2.0 style with Mapped types
- Optional fields
- Timestamps
"""

from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import TimestampMixin, PrimaryKeyMixin


class Item(Base, TimestampMixin, PrimaryKeyMixin):
    """
    Item model representing items owned by users.

    Attributes:
        id: Primary key (from PrimaryKeyMixin)
        title: Item title
        description: Item description (optional)
        owner_id: Foreign key to users table
        is_published: Whether the item is published
        created_at: Timestamp of item creation (from TimestampMixin)
        updated_at: Timestamp of last update (from TimestampMixin)
        owner: Relationship to the user who owns this item
    """
    __tablename__ = "items"

    # Item information
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Foreign key to users
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"