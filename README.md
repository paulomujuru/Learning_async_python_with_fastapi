# Learning Async Python with FastAPI

A comprehensive project to learn asynchronous programming in Python using FastAPI.

## Overview

This project demonstrates various async patterns and techniques in Python, including:
- Basic async/await syntax
- Concurrent API requests
- asyncio.gather for parallel execution
- Background tasks
- Sequential vs concurrent processing

## Project Structure

```
.
├── main.py                    # Main FastAPI application
├── requirements.txt           # Project dependencies
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # API route examples
│   ├── models/
│   │   └── __init__.py
│   └── services/
│       ├── __init__.py
│       └── async_service.py  # Async service functions
└── .venv/                    # Virtual environment
```

## Setup

1. Activate the virtual environment:
```bash
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Available Endpoints

### Basic Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check

### Async Examples
- `GET /api/async-hello` - Simple async endpoint with delay
- `GET /api/simulate-task/{task_id}` - Simulate async task processing
- `GET /api/concurrent-fetch` - Demonstrate concurrent HTTP requests
- `GET /api/gather-example` - Demonstrate asyncio.gather
- `POST /api/background-task` - Create a background task

## Learning Resources

### Key Concepts Covered

1. **Async/Await Basics** - Understanding coroutines and async functions
2. **Concurrent Execution** - Running multiple async operations in parallel
3. **asyncio.gather** - Collecting results from multiple coroutines
4. **HTTP Client Requests** - Using httpx for async HTTP requests
5. **Background Tasks** - Fire-and-forget async operations

### Example Usage

```python
# Test the concurrent fetch endpoint
curl http://localhost:8000/api/concurrent-fetch

# Simulate a task
curl http://localhost:8000/api/simulate-task/1

# Test asyncio.gather
curl http://localhost:8000/api/gather-example
```

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pydantic** - Data validation using Python type hints
- **httpx** - Async HTTP client
- **aiofiles** - Async file operations

## Next Steps

- Add database integration with async drivers (e.g., asyncpg, motor)
- Implement WebSocket connections
- Add async middleware examples
- Create more complex async patterns (semaphores, locks, etc.)
- Add unit tests with pytest-asyncio

## License

MIT