from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow_api.database.models import Task


async def get_all_tasks(db: AsyncSession):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_tasks(
    db: AsyncSession,
    page: int,
    limit: int,
    priority: int | None = None,
    status: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
):
    query = select(Task)

    # Filtering
    if priority is not None:
        query = query.where(Task.priority == priority)

    if status is not None:
        query = query.where(Task.status == status)

    # Sorting
    sort_column = {
        "id": Task.id,
        "priority": Task.priority,
        "title": Task.title,
        "status": Task.status,
    }[sort_by]

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Total count
    count_query = select(func.count()).select_from(query.subquery())

    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    # Pagination
    offset = (page - 1) * limit

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)

    tasks = result.scalars().all()

    return tasks, total


async def get_task_by_id(
    db: AsyncSession,
    task_id: int
):
    result = await db.execute(
        select(Task).where(Task.id == task_id)
    )
    return result.scalar_one_or_none()

async def create_task(
    db: AsyncSession,
    task: Task
):
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task

async def delete_task(
    db: AsyncSession,
    task: Task
):
    await db.delete(task)
    await db.commit()

async def update_task(
    db: AsyncSession,
    task: Task
):
    await db.commit()
    await db.refresh(task)

    return task    