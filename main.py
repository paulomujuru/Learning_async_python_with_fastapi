import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router as async_examples_router
from app.api.users import router as users_router
from app.api.items import router as items_router
from app.core.database import init_db, close_db
from app.models import User, Item  # Import models to register them with SQLAlchemy


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for database initialization and cleanup.

    This replaces the deprecated @app.on_event("startup") and @app.on_event("shutdown")
    """
    # Startup: Initialize database
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")

    yield

    # Shutdown: Close database connections
    print("Closing database connections...")
    await close_db()
    print("Database connections closed!")


app = FastAPI(
    title="Learning Async Python with FastAPI",
    description="A project to learn asynchronous programming with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# Include API routes
app.include_router(async_examples_router, prefix="/api", tags=["Async Examples"])
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(items_router, prefix="/api", tags=["Items"])


@app.get("/")
async def root():
    """Basic async endpoint"""
    return {"message": "Welcome to Learning Async Python with FastAPI!"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)