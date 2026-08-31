import pytest

from app.exceptions import (InvalidTaskTitleError , TaskNotFoundError)

def test_should_create_task(service):

    task = service.create_task("test automatico")

    assert task is not None
    assert task.id is not None
    assert task.id == 1
    assert task.title == "test automatico"
    assert task.completed is False

def test_should_trim_task_title(service):
    task = service.create_task("    test automatico ")
    assert task.title == "test automatico"
    assert task.completed is False
    assert task.id == 1

def test_should_not_create_task(service):
    with pytest.raises(
            InvalidTaskTitleError
    ):
        service.create_task("")

def test_should_reject_blank_title(service):
    with pytest.raises(InvalidTaskTitleError):
        service.create_task("       ")

def test_should_list_tasks(service):
    service.create_task("test automatico 1")
    service.create_task("test automatico 2")

    tasks = service.list_tasks()

    assert len(tasks) == 2

    task = tasks[0]
    assert task.title == "test automatico 1"
    assert task.completed is False
    assert task.id == 1

    task = tasks[1]
    assert task.title == "test automatico 2"
    assert task.completed is False
    assert task.id == 2

def test_should_complete_task(service):
    task = service.create_task("test automatico 1")

    completed_task = service.complete_task(task.id)

    assert completed_task.completed is True

def test_should_raise_error_when_completing_unknown_task(service):
    with pytest.raises(TaskNotFoundError):
        service.complete_task(99999)

def test_should_delete_task(service):
    task = service.create_task("test automatico 1")

    service.delete_task(task.id)

    tasks = service.list_tasks()

    assert len(tasks) == 0
    assert tasks == []

def test_should_raise_error_when_deleting_unknown_task(service):
    with pytest.raises(TaskNotFoundError):
        service.delete_task(99999)

