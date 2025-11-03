import asyncio
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Learning Async Python with FastAPI",
    description="A project to learn asynchronous programming with FastAPI",
    version="1.0.0"
)

# Include API routes
app.include_router(router, prefix="/api", tags=["examples"])


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