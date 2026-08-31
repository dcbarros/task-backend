from app.models import Task


class FakeTaskRepository:

    def __init__(self):
        self.tasks: list[Task] = []
        self.next_id = 1

    def list_all(self) -> list[Task]:
        return self.tasks.copy()

    def get_by_id(
        self,
        task_id: int
    ) -> Task | None:

        for task in self.tasks:

            if task.id == task_id:
                return task

        return None

    def create(
        self,
        title: str
    ) -> Task:

        task = Task(
            title=title,
            completed=False
        )

        task.id = self.next_id

        self.next_id += 1

        self.tasks.append(task)

        return task

    def complete(
        self,
        task: Task
    ) -> Task:

        task.completed = True

        return task

    def delete(
        self,
        task: Task
    ) -> None:

        self.tasks.remove(task)