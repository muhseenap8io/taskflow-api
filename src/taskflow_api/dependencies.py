from fastapi import Header,HTTPException,Depends
from collections.abc import Generator
# from sqlalchemy.orm import Session

from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from taskflow_api.database.database import AsyncSessionLocal
from taskflow_api.config.settings import settings
# from taskflow_api.database.database import SessionLocal

# def get_db()-> Generator[Session,None,None]:
#     db=SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()   

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db

async def verify_api_key(x_api_key:str|None=Header(default=None)):
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or misssing API key"
        )
    return x_api_key

async def get_current_user(api_key:str=Depends(verify_api_key)):
    return {
        "id": 1,
        "name": "Admin User",
        "role": "admin",
    }

async def get_user_agent(user_agent:str| None = Header(default=None)):
    return user_agent


async def get_request_id(x_request_id:str|None=Header(default=None)):
    return x_request_id

