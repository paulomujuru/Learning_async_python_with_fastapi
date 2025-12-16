"""
Common exception handlers and HTTP error utilities.

This module provides reusable error handling utilities to reduce duplication in API endpoints.
"""

from typing import Optional
from fastapi import HTTPException, status


def raise_not_found(resource_name: str = "Resource", resource_id: Optional[int] = None) -> None:
    """
    Raise a 404 Not Found HTTP exception.

    Args:
        resource_name: Name of the resource (e.g., "User", "Item")
        resource_id: Optional ID of the resource

    Raises:
        HTTPException: 404 Not Found error
    """
    detail = f"{resource_name} not found"
    if resource_id is not None:
        detail = f"{resource_name} with id {resource_id} not found"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def raise_bad_request(detail: str) -> None:
    """
    Raise a 400 Bad Request HTTP exception.

    Args:
        detail: Error message describing what went wrong

    Raises:
        HTTPException: 400 Bad Request error
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def raise_conflict(resource_name: str, field_name: str, field_value: str) -> None:
    """
    Raise a 409 Conflict HTTP exception for duplicate resource.

    Args:
        resource_name: Name of the resource (e.g., "User", "Item")
        field_name: Name of the field causing conflict (e.g., "email", "username")
        field_value: Value that already exists

    Raises:
        HTTPException: 409 Conflict error
    """
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{resource_name} with {field_name} '{field_value}' already exists"
    )


def raise_unauthorized(detail: str = "Not authenticated") -> None:
    """
    Raise a 401 Unauthorized HTTP exception.

    Args:
        detail: Error message

    Raises:
        HTTPException: 401 Unauthorized error
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_forbidden(detail: str = "Not enough permissions") -> None:
    """
    Raise a 403 Forbidden HTTP exception.

    Args:
        detail: Error message

    Raises:
        HTTPException: 403 Forbidden error
    """
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )