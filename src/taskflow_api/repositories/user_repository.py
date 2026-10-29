from sqlalchemy.ext.asyncio import AsyncSession

from taskflow_api.database.models import User


async def create_user(
    db: AsyncSession,
    user: User
):
    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user