from fastapi import FastAPI, HTTPException, status, Request
from typing import List
from schemas import (
    TodoListCreate,
    TodoListResponse,
    TodoTaskCreate,
    TodoTaskResponse,
    TodoTaskUpdate,
)
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

db_lists: list[dict] = [
    {"id": 1, "name": "personal"},
    {"id": 2, "name": "work"},
]


db_tasks: list[dict] = [
    {"id": 1, "title": "seize the day", "list_id": 1},
    {"id": 2, "title": "be the force", "list_id": 1},
]


@app.get("/api/lists", response_model=List[TodoListResponse])
def get_lists():
    return db_lists


@app.post(
    "/api/lists", status_code=status.HTTP_201_CREATED, response_model=TodoListResponse
)
def create_list(data: TodoListCreate):
    new_id = len(db_lists) + 1

    new_list = TodoListResponse(id=new_id, **data.model_dump())
    db_lists.append(new_list)
    return new_list


@app.get("/api/tasks", response_model=list[TodoTaskResponse])
def get_tasks():

    try:
        return db_tasks
    except ValidationError as e:
        return {"error": e}


@app.post("/api/tasks", response_model=TodoTaskResponse)
def create_task(data: TodoTaskCreate):
    new_id = len(db_tasks) + 1

    data = data.model_dump()
    list_id = data.get("list_id")
    list_exists = False

    for list in db_lists:
        if list.get("id") == list_id:
            list_exists = True
            break

    if not list_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo list with ID {list_id} does not exist.",
        )

    new_task = TodoTaskResponse(id=new_id, **data)
    db_tasks.append(new_task)

    return new_task


@app.patch("/api/tasks/{task_id}", response_model=TodoTaskResponse)
def update_task(task_id: int, data: TodoTaskUpdate):

    task_to_update = None

    for task in db_tasks:
        if task.get("id") == task_id:
            task_to_update = task
            break

    if task_to_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo task with ID {task_id} does not exist.",
        )

    updated_fields = data.model_dump(exclude_unset=True)

    for key, value in updated_fields.items():
        task_to_update[key] = value

    return task_to_update


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):

    for task in db_tasks:
        if task.get("id") == task_id:
            db_tasks.remove(task)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo task with ID {task_id} does not exist.",
    )


# @app.exception_handler(StarletteHTTPException)
# def http_exception_handler(request: Request, exception: StarletteHTTPException):
#     message = exception.detail if exception.detail else "An error occured."
#     return JSONResponse(status_code=exception.status_code, content={"detail": message})


# @app.exception_handler(ResponseValidationError)
# def validation_exception_handler(request: Request, exception: ResponseValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
#         content={"detail": exception.errors()},
#     )
