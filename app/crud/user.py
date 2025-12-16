"""
CRUD operations for User model.

This module contains async functions to interact with the User table.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    CRUD operations for User model.

    Inherits common CRUD operations from CRUDBase and adds user-specific methods.
    """

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by email address.

        Args:
            db: Database session
            email: Email address to search for

        Returns:
            User object or None if not found
        """
        return await self.get_by_field(db, "email", email)

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        Get a user by username.

        Args:
            db: Database session
            username: Username to search for

        Returns:
            User object or None if not found
        """
        return await self.get_by_field(db, "username", username)


# Create a singleton instance
crud_user = CRUDUser(User)

# Expose functions for backward compatibility
get_user = crud_user.get
get_user_by_email = crud_user.get_by_email
get_user_by_username = crud_user.get_by_username
get_users = crud_user.get_multi
create_user = crud_user.create
update_user = crud_user.update
delete_user = crud_user.delete