from pydantic import BaseModel, ConfigDict


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TaskCreate(BaseModel):
    title: str
    completed: bool = False