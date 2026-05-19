from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from functools import partial
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    INPROGRESS = "in_progress"


class TodoListCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class TodoListResponse(TodoListCreate):
    id: int

    # model_config = ConfigDict(from_attributes=True)


class TodoTaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    description: str | None = None
    list_id: int


class TodoTaskResponse(TodoTaskCreate):
    id: int
    status: TaskStatus = TaskStatus.PENDING
    createAt: datetime = Field(
        default_factory=partial(datetime.now, timezone.utc), frozen=True
    )

    # model_config = ConfigDict(from_attributes=True)


class TodoTaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=50)
    status: Optional[TaskStatus] = None
    description: Optional[str] = None
