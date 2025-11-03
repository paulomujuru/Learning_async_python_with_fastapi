import asyncio
from fastapi import APIRouter, HTTPException
from typing import List
import httpx
from app.services.async_service import (
    simulate_async_task,
    fetch_data_concurrently,
    process_with_asyncio_gather, background_worker
)

router = APIRouter()


@router.get("/async-hello")
async def async_hello():
    """Simple async endpoint"""
    await asyncio.sleep(1)
    return {"message": "Hello from async endpoint!"}


@router.get("/simulate-task/{task_id}")
async def simulate_task(task_id: int):
    """
    Simulate an async task with delay
    Example: GET /api/simulate-task/1
    """
    result = await simulate_async_task(task_id)
    return result


@router.get("/concurrent-fetch")
async def concurrent_fetch():
    """
    Demonstrates concurrent async HTTP requests
    Fetches data from multiple URLs concurrently.
    """
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3",
    ]

    try:
        results = await fetch_data_concurrently(urls)
        return {
            "message": "Fetched data concurrently",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gather-example")
async def gather_example():
    """
    Demonstrates asyncio.gather for parallel execution
    Runs multiple async tasks in parallel
    """
    results = await process_with_asyncio_gather()
    return {
        "message": "Processed tasks with asyncio.gather",
        "results": results
    }


@router.post("/background-task")
async def create_background_task():
    """
    Example of a background task (fire and forget)
    The task runs in the background while response is returned immediately
    """
    asyncio.create_task(background_worker())
    return {"message": "Background task started"}
