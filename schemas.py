from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
from datetime import datetime, timezone
from functools import partial


class TodoListBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)


class TodoListResponse(TodoListBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TodoTaskBase(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    description: str | None = None
    status: Literal["pending", "completed"] = "pending"


class TodoTaskCreate(TodoTaskBase):
    list_id: int


class TodoTaskResponse(TodoTaskBase):
    id: int
    list_id: int
    createAt: datetime = Field(
        default_factory=partial(datetime.now, timezone.utc), frozen=True
    )

    model_config = ConfigDict(from_attributes=True)
