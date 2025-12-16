"""
Base class for all SQLAlchemy models.

This module provides the declarative base that all database models will inherit from.
Using SQLAlchemy 2.0 style with declarative mapping.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.

    All models should inherit from this class:

    Example:
        from app.db.base import Base
        from sqlalchemy.orm import Mapped, mapped_column
        from sqlalchemy import Integer, String

        class User(Base):
            __tablename__ = "users"

            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            name: Mapped[str] = mapped_column(String(100))
    """
    pass