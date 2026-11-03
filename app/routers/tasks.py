from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        completed=task.completed,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if existing_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_task, field, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task