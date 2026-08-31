import pytest

from app.service import TaskService
from tests.unit.fakes import FakeTaskRepository


@pytest.fixture
def repository():
    return FakeTaskRepository()


@pytest.fixture
def service(repository):
    return TaskService(repository)