import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client(tmp_path):

    database_file = (
        tmp_path / "test_task_pilot.db"
    )

    database_url = (
        f"sqlite:///{database_file}"
    )

    test_engine = create_engine(
        database_url,
        connect_args={
            "check_same_thread": False
        }
    )

    TestSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False
    )

    Base.metadata.create_all(
        bind=test_engine
    )

    def override_get_db():

        db = TestSessionLocal()

        try:
            yield db

        finally:
            db.close()

    app.dependency_overrides[
        get_db
    ] = override_get_db

    test_client = TestClient(app)

    yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(
        bind=test_engine
    )

    test_engine.dispose()