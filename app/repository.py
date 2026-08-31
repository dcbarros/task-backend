from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task


class TaskRepository:

    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Task]:

        statement = select(Task).order_by(Task.id)

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_id(self, task_id: int) -> Task | None:

        return self.db.get(
            Task,
            task_id
        )

    def create(self, title: str) -> Task:

        task = Task(
            title=title,
            completed=False
        )

        self.db.add(task)

        self.db.commit()

        self.db.refresh(task)

        return task

    def complete(self, task: Task) -> Task:

        task.completed = True

        self.db.commit()

        self.db.refresh(task)

        return task

    def delete(self, task: Task) -> None:

        self.db.delete(task)

        self.db.commit()