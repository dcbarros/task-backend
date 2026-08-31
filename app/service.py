from app.exceptions import (
    InvalidTaskTitleError,
    TaskNotFoundError
)
from app.models import Task
from app.repository import TaskRepository


class TaskService:

    def __init__(
        self,
        repository: TaskRepository
    ):
        self.repository = repository

    def list_tasks(self) -> list[Task]:

        return self.repository.list_all()

    def create_task(
        self,
        title: str
    ) -> Task:

        normalized_title = title.strip()

        if not normalized_title:
            raise InvalidTaskTitleError()

        return self.repository.create(
            normalized_title
        )

    def complete_task(
        self,
        task_id: int
    ) -> Task:

        task = self.repository.get_by_id(
            task_id
        )

        if task is None:
            raise TaskNotFoundError()

        return self.repository.complete(
            task
        )

    def delete_task(
        self,
        task_id: int
    ) -> None:

        task = self.repository.get_by_id(
            task_id
        )

        if task is None:
            raise TaskNotFoundError()

        self.repository.delete(task)