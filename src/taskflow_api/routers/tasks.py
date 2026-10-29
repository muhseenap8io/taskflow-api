from fastapi import APIRouter,Depends,HTTPException,Query
from taskflow_api.schemas.task import TaskCreate,TaskCreateResponse
from taskflow_api.dependencies import get_user_agent,get_request_id
# ,get_db
from sqlalchemy.orm import Session
from taskflow_api.database.models import Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow_api.dependencies import get_async_db,verify_api_key,get_current_user
from taskflow_api.services.task_service import (get_all_tasks,get_task_by_id,create_task,update_task,delete_task)
from taskflow_api.schemas.task import TaskListResponse
from taskflow_api.services.task_service import get_paginated_tasks


router = APIRouter(
    # prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(verify_api_key)]
)


@router.get("/me")
async def get_me(
    current_user: dict = Depends(get_current_user),
):
    return current_user

@router.get("/tasks", response_model=TaskListResponse)
async def get_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    priority: int | None = Query(default=None, ge=1, le=5),
    status: str | None = None,
    sort_by: str = Query(
        default="id",
        pattern="^(id|priority|title|status)$"
    ),
    order: str = Query(
        default="asc",
        pattern="^(asc|desc)$"
    ),
    db: AsyncSession = Depends(get_async_db),
):
    return await get_paginated_tasks(
        db=db,
        page=page,
        limit=limit,
        priority=priority,
        status=status,
        sort_by=sort_by,
        order=order,
    )

@router.get("/db-test")
async def db_test(db:AsyncSession = Depends(get_async_db)):
    print("DATABASE AsyncSession:", db)

    tasks= await db.query(Task).all()

    return {
         "tasks": tasks,
         "count": len(tasks)

    }


# @router.get("/tasks", response_model=list[TaskCreateResponse])
# async def get_tasks(db: AsyncSession = Depends(get_async_db)):
#     tasks = await get_all_tasks(db)
#     return tasks


@router.get("/tasks/{task_id}", response_model=TaskCreateResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db),
    api_key:str = Depends(verify_api_key)
):
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )

    task = await get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# @router.post("/tasks", response_model=TaskCreateResponse)
# async def create_task(
#     task: TaskCreate,
#     db: AsyncSession = Depends(get_async_db)
# ):
#     new_task = Task(
#         title=task.title,
#         description=task.description,
#         priority=task.priority
#     )
#     try:
#       db.add(new_task)

#     #   raise Exception("Something went wrong")

#       await db.commit()
#     except Exception:
#         db.rollback()
    #     raise  

    # await db.refresh(new_task)

    # return new_task

@router.post("/tasks", response_model=TaskCreateResponse)
async def create_task_endpoint(
    task: TaskCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await create_task(db, task)

@router.put("/tasks/{task_id}", response_model=TaskCreateResponse)
async def update_created_task(
    task_id: int,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_async_db)
):
    result = db.execute(
        select(Task).where(Task.id == task_id)
    )

    task = await update_task(db,task_id,task_data)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # task.title = task_data.title
    # task.description = task_data.description
    # task.priority = task_data.priority

    # db.commit()
    # db.refresh(task)

    return task


@router.delete("/tasks/{task_id}")
async def delete_created_task(
    task_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    

    task = await delete_task(db,task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

   

    return {
        "message": "Task deleted successfully"
    }