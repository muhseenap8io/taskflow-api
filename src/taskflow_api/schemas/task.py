from pydantic import BaseModel,Field

class TaskCreate(BaseModel):
    title:str = Field(min_length=3,max_length=100)
    description:str | None =None
    priority:int=Field(default=1,ge=1,le=5)
    user_id: int


class TaskCreateResponse(BaseModel):
    id:int
    title:str
    description:str | None
    priority:int 
    status: str
    user_id: int   

class TaskListResponse(BaseModel):
    items: list[TaskCreateResponse]
    page: int
    limit: int
    total: int
    pages: int    