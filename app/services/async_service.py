import asyncio
import httpx
from typing import List, Dict, Any


async def simulate_async_task(task_id: int) -> Dict[str, Any]:
    """
    Simulates an async task with a delay
    Useful for understanding async behavior
    """
    print(f"Starting task {task_id}")
    await asyncio.sleep(2)
    print(f"Completed task {task_id}")
    return {
        "task_id": task_id,
        "status": "completed",
        "message": f"Task {task_id} processed successfully"
    }


async def fetch_url(client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
    """
    Fetches data from a single URL asynchronously
    """
    try:
        response = await client.get(url)
        response.raise_for_status()
        return {
            "url": url,
            "status": response.status_code,
            "data": response.json()
        }
    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


async def fetch_data_concurrently(urls: List[str]) -> List[Dict[str, Any]]:
    """
    Fetches data from multiple URLs concurrently using asyncio.gather
    This demonstrates how async can improve performance for I/O-bound operations
    """
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results


async def async_operation_1():
    """First async operation"""
    await asyncio.sleep(1)
    return "Operation 1 completed"


async def async_operation_2():
    """Second async operation"""
    await asyncio.sleep(1.5)
    return "Operation 2 completed"


async def async_operation_3():
    """Third async operation"""
    await asyncio.sleep(0.5)
    return "Operation 3 completed"


async def process_with_asyncio_gather() -> List[str]:
    """
    Demonstrates asyncio.gather for running multiple async operations in parallel
    All operations run concurrently, total time is determined by the slowest operation
    """
    results = await asyncio.gather(
        async_operation_1(),
        async_operation_2(),
        async_operation_3()
    )
    return results

async def background_worker():
    """Simulates a background worker"""
    await asyncio.sleep(5)
    print("Background task completed!")


async def sequential_processing(items: List[int]) -> List[int]:
    """
    Example of sequential async processing (one after another)
    Use when operations depend on each other
    """
    results = []
    for item in items:
        await asyncio.sleep(0.5)
        results.append(item * 2)
    return results


async def concurrent_processing(items: List[int]) -> List[int]:
    """
    Example of concurrent async processing (all at once)
    Use when operations are independent
    """
    async def process_item(item: int) -> int:
        await asyncio.sleep(0.5)
        return item * 2

    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results