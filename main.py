from fastapi import FastAPI, HTTPException, status, Request
from typing import List
from schemas import TodoTaskResponse, TodoListResponse, TodoListBase
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


@app.get("/api/todolists", response_model=list[TodoListResponse])
def get_todo_lists():
    return db_lists


@app.post(
    "/api/lists", response_model=TodoListResponse, status_code=status.HTTP_201_CREATED
)
def create_list(data: TodoListBase):
    new_id = len(db_tasks) + 1

    new_list = TodoListResponse(id=new_id, **data.model_dump())
    db_lists.append(new_list)
    return new_list


@app.get("/api/tasks", response_model=list[TodoTaskResponse])
def get_tasks():

    try:
        return db_tasks
    except ValidationError as e:
        return {"error": e}


@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = exception.detail if exception.detail else "An error occured."

    return JSONResponse(status_code=exception.status_code, content={"detail": message})


@app.exception_handler(ResponseValidationError)
def validation_exception_handler(request: Request, exception: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exception.errors()},
    )
