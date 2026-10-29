from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
import time
import uuid
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from taskflow_api.routers import tasks,async_demo,users
from taskflow_api.config.settings import settings

from taskflow_api.exceptions import TaskNotFoundException
# from taskflow_api.database.database import Base, engine
# from taskflow_api.database import models

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("🚀 Application starting...")

    # app.state.some_resource = "My expensive resource"

    # print("Resource initialized")

    # Base.metadata.create_all(bind=engine)
    # async with engine.begin() as conn:
    #  await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    yield

    # print("Closing resource...")
    # app.state.some_resource = None

    print("🛑 Application shutting down...")

app = FastAPI(title=settings.app_name,lifespan=lifespan)

@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration:.4f}"

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"status={response.status_code} "
        f"time={duration:.4f}s "
        f"request_id={request_id}"
    )

    return response

@app.exception_handler(TaskNotFoundException)
async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "error": "TASK_NOT_FOUND",
            "message": f"Task with id {exc.task_id} was not found",
            "path": request.url.path,
        },
    )

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    print(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Something went wrong",
            "path": request.url.path,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Invalid request parameters",
            "details": exc.errors(),
            "path": request.url.path,
        },
    )

app.include_router(tasks.router)
app.include_router(async_demo.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "TaskFlow API is running"}


