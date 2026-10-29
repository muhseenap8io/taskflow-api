import asyncio
import time

from fastapi import APIRouter

router = APIRouter()



async def fetch_users():
    print("Fetching users...")
    await asyncio.sleep(3)
    print("Users fetched")

    return ["Alice", "Bob"]


async def fetch_tasks():
    print("Fetching tasks...")
    await asyncio.sleep(3)
    print("Tasks fetched")

    return ["Task 1", "Task 2"]


@router.get("/sequential")
async def sequential_task():
    start = time.perf_counter()

    users = await fetch_users()
    tasks = await fetch_tasks()

    elapsed = time.perf_counter() - start

    return {
        "users":users,
        "tasks":tasks,
        "elapsed_time":elapsed
    }

@router.get("/concurrent")
async def concurrent_task():
    start = time.perf_counter()

    users,tasks = await asyncio.gather(
        fetch_users(),
        fetch_tasks()
    )

    elapsed = time.perf_counter() - start
    
    return {
            "users":users,
            "tasks":tasks,
            "elapsed_time":elapsed
        }


@router.get("/async-test")
async def async_test():
    print("ASYNC START")

    await asyncio.sleep(10)

    print("ASYNC END")

    return {"message": "Async wait is over"}


@router.get("/sync-test")
def sync_test():
    print("SYNC START")

    time.sleep(10)

    print("SYNC END")

    return {"message": "Sync wait is over"}


@router.get("/blocking-test")
async def blocking_test():
    print("BLOCKING START")

    time.sleep(10)

    print("BLOCKING END")

    return {"message": "Blocking wait is over"}