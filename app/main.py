from fastapi import FastAPI

from app.routers import tasks

app = FastAPI(
    title="Task Manager API",
    description="API for managing tasks",
    version="1.0.0",
)

app.include_router(tasks.router)