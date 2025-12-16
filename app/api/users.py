"""
API routes for User operations.

This module demonstrates:
- CRUD operations with async database
- Request/response validation with Pydantic
- Error handling
- Dependency injection with FastAPI
"""

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import raise_bad_request, raise_not_found
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud import user as crud_user

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.

    Args:
        user: User data from request body
        db: Database session (injected)

    Returns:
        Created user data

    Raises:
        HTTPException: 400 if username or email already exists
    """
    # Check if username already exists
    db_user = await crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise_bad_request("Username already registered")

    # Check if email already exists
    db_user = await crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise_bad_request("Email already registered")

    return await crud_user.create_user(db=db, obj_in=user)


@router.get("/users", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    """
    Retrieve a list of users with pagination.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100, max: 100)
        db: Database session (injected)

    Returns:
        List of users
    """
    users = await crud_user.get_users(db, skip=skip, limit=min(limit, 100))
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get a specific user by ID.

    Args:
        user_id: User ID
        db: Database session (injected)

    Returns:
        User data

    Raises:
        HTTPException: 404 if user not found
    """
    db_user = await crud_user.get_user(db, id=user_id)
    if db_user is None:
        raise_not_found("User", user_id)
    return db_user


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Update a user's information.

    Args:
        user_id: User ID
        user: Updated user data (partial updates allowed)
        db: Database session (injected)

    Returns:
        Updated user data

    Raises:
        HTTPException: 404 if user not found
        HTTPException: 400 if username or email already taken
    """
    # Check if username is being changed and is already taken
    if user.username:
        existing_user = await crud_user.get_user_by_username(db, username=user.username)
        if existing_user and existing_user.id != user_id:
            raise_bad_request("Username already taken")

    # Check if email is being changed and is already taken
    if user.email:
        existing_user = await crud_user.get_user_by_email(db, email=user.email)
        if existing_user and existing_user.id != user_id:
            raise_bad_request("Email already taken")

    db_user = await crud_user.update_user(db, id=user_id, obj_in=user)
    if db_user is None:
        raise_not_found("User", user_id)
    return db_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a user.

    Args:
        user_id: User ID
        db: Database session (injected)

    Raises:
        HTTPException: 404 if user not found
    """
    success = await crud_user.delete_user(db, id=user_id)
    if not success:
        raise_not_found("User", user_id)