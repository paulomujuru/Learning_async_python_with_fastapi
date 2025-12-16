"""
Database connection and session management.

This module handles:
- Async database engine creation
- Session factory for creating async sessions
- Dependency injection for FastAPI routes
- Database initialization and cleanup
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool, StaticPool

from app.core.config import settings
from app.db.base import Base


# Create async engine
# For SQLite, we use StaticPool to avoid threading issues
# For PostgreSQL, we use NullPool or default pooling
def get_engine() -> AsyncEngine:
    """
    Create and configure the async database engine.

    Returns:
        AsyncEngine: Configured async engine for database operations
    """
    # Special handling for SQLite
    if settings.DATABASE_URL.startswith("sqlite"):
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            future=True,
            connect_args={"check_same_thread": False},  # Needed for SQLite
            poolclass=StaticPool,  # Use StaticPool for SQLite
        )
    else:
        # PostgreSQL or other databases
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DATABASE_ECHO,
            future=True,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=5,  # Connection pool size
            max_overflow=10,  # Max overflow connections
        )
    return engine


# Create engine instance
engine = get_engine()

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autocommit=False,  # Manual transaction control
    autoflush=False,  # Manual flush control
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function that provides a database session.

    This function is used with FastAPI's Depends() to inject a database
    session into route handlers. It automatically handles session lifecycle:
    - Creates a new session
    - Yields it to the route handler
    - Commits on success
    - Rolls back on error
    - Always closes the session

    Usage:
        from fastapi import Depends
        from sqlalchemy.ext.asyncio import AsyncSession
        from app.core.database import get_db

        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            # Use db session here
            result = await db.execute(select(Item))
            return result.scalars().all()

    Yields:
        AsyncSession: Database session for the request
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize the database by creating all tables.

    This function should be called during application startup.
    It creates all tables defined in models that inherit from Base.

    Usage:
        from app.core.database import init_db

        @app.on_event("startup")
        async def startup_event():
            await init_db()

    Note:
        In production, use Alembic migrations instead of this function.
        This is useful for development and testing.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db() -> None:
    """
    Drop all database tables.

    WARNING: This is a destructive operation that will delete all data!
    Only use this for testing or development.

    Usage:
        from app.core.database import drop_db

        # Use with caution!
        await drop_db()
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def close_db() -> None:
    """
    Close the database engine and all connections.

    This function should be called during application shutdown.

    Usage:
        from app.core.database import close_db

        @app.on_event("shutdown")
        async def shutdown_event():
            await close_db()
    """
    await engine.dispose()


# For testing and development: Create session without dependency injection
async def get_session() -> AsyncSession:
    """
    Create a new database session for manual use.

    This is useful for testing or scripts where you need a session
    outside of FastAPI's dependency injection system.

    Usage:
        from app.core.database import get_session

        async def my_function():
            async with await get_session() as session:
                result = await session.execute(select(User))
                users = result.scalars().all()

    Returns:
        AsyncSession: New database session
    """
    return AsyncSessionLocal()