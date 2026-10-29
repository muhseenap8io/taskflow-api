from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow_api.dependencies import get_async_db
from taskflow_api.schemas.user import UserCreate, UserResponse
from taskflow_api.services.user_service import create_user


router = APIRouter()


@router.post("/users", response_model=UserResponse)
async def create_user_endpoint(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_db)
):
    return await create_user(db, user)