import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from database.session import get_session
from main import app


@pytest.fixture
def client(tmp_path):
    test_database = tmp_path / "test.db"

    test_engine = create_engine(
        f"sqlite:///{test_database}",
        connect_args={"check_same_thread": False},
    )

    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_product():
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 99.99,
        "stock": 10,
    }