from sqlalchemy.ext.asyncio import AsyncSession
from taskflow_api.schemas.task import TaskCreate
from taskflow_api.database.models import Task
from taskflow_api.repositories.task_repository import (
    get_all_tasks as get_all_tasks_repo,
    get_task_by_id as get_task_by_id_repo,
    create_task as create_task_repo, update_task as update_task_repo,
     delete_task as delete_task_repo,
)
import math
from taskflow_api.exceptions import TaskNotFoundException
from taskflow_api.repositories.task_repository import get_tasks


async def get_paginated_tasks(
    db: AsyncSession,
    page: int,
    limit: int,
    priority: int | None = None,
    status: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
):
    tasks, total = await get_tasks(
        db=db,
        page=page,
        limit=limit,
        priority=priority,
        status=status,
        sort_by=sort_by,
        order=order,
    )

    pages = math.ceil(total / limit) if total > 0 else 0

    return {
        "items": tasks,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": pages,
    }


async def get_all_tasks(db: AsyncSession):
    return await get_all_tasks_repo(db)


async def get_task_by_id(
    db: AsyncSession,
    task_id: int
):
    task = await get_task_by_id_repo(db, task_id)
    if task is None:
        raise TaskNotFoundException(task_id)
    return task


async def create_task(
    db: AsyncSession,
    task_data: TaskCreate
):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        user_id=task_data.user_id
    )

    return await create_task_repo(db, new_task)

async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskCreate
):
    task = await get_task_by_id_repo(db, task_id)

    if task is None:
        return None

    task.title = task_data.title
    task.description = task_data.description
    task.priority = task_data.priority

    return await update_task_repo(db, task)

async def delete_task(
    db: AsyncSession,
    task_id: int
):
    task = await get_task_by_id_repo(db, task_id)

    if task is None:
        return False

    await delete_task_repo(db, task)

    return True