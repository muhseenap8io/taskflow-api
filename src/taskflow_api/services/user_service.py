from sqlalchemy.ext.asyncio import AsyncSession

from taskflow_api.database.models import User
from taskflow_api.repositories.user_repository import (
    create_user as create_user_repo,
)
from taskflow_api.schemas.user import UserCreate


async def create_user(
    db: AsyncSession,
    user_data: UserCreate
):
    user = User(
        name=user_data.name
    )

    return await create_user_repo(db, user)