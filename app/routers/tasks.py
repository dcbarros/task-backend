from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import (
    InvalidTaskTitleError,
    TaskNotFoundError
)
from app.repository import TaskRepository
from app.schemas import (
    TaskCreate,
    TaskResponse
)
from app.service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


DbSession = Annotated[
    Session,
    Depends(get_db)
]


def get_task_service(
    db: DbSession
) -> TaskService:

    repository = TaskRepository(db)

    return TaskService(repository)


TaskServiceDependency = Annotated[
    TaskService,
    Depends(get_task_service)
]


@router.get(
    "",
    response_model=list[TaskResponse]
)
def list_tasks(
    service: TaskServiceDependency
):

    return service.list_tasks()


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    payload: TaskCreate,
    service: TaskServiceDependency
):

    try:

        return service.create_task(
            payload.title
        )

    except InvalidTaskTitleError:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be blank"
        )


@router.patch(
    "/{task_id}/complete",
    response_model=TaskResponse
)
def complete_task(
    task_id: int,
    service: TaskServiceDependency
):

    try:

        return service.complete_task(
            task_id
        )

    except TaskNotFoundError:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    service: TaskServiceDependency
):

    try:

        service.delete_task(
            task_id
        )

        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )

    except TaskNotFoundError:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )