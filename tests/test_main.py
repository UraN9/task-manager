import pytest
from app import main

from fastapi.testclient import TestClient

from app.database import Base, get_db , test_engine

from sqlalchemy.orm import Session
from sqlalchemy import text

client = TestClient(main.app)
    
@pytest.fixture(scope="function", autouse=True)
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with test_engine.connect() as connection:
        current_db = connection.execute(
            text("SELECT current_database()")
        ).scalar_one()

    if current_db != "task_manager_test":
        raise RuntimeError(
            f"Tests are running against '{current_db}' instead of 'task_manager_test'!"
        )

    Base.metadata.create_all(bind=test_engine)

    try:
        yield
    finally:
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def override_db(db_session):
    def _override_get_db():
        yield db_session

    main.app.dependency_overrides[get_db] = _override_get_db

    yield

    main.app.dependency_overrides.clear()


def test_get_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all(
        "id" in task and 
        "title" in task and 
        "completed" in task for task in response.json()
        )
    assert all(
        isinstance(task["id"], int) and 
        isinstance(task["title"], str) and 
        isinstance(task["completed"], bool) for task in response.json()
        )

def test_get_task_by_id():
    new_task = {
        "title": "Test task",
        "completed": False
    }

    create_response = client.post("/tasks/", json=new_task)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == new_task["title"]
    assert response.json()["completed"] == new_task["completed"]

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_create_new_task():
    new_task = {
        "title": "New task",
        "completed": False
    }

    create_response = client.post("/tasks/", json=new_task)

    assert create_response.status_code == 201
    assert create_response.json()["title"] == new_task["title"]
    assert create_response.json()["completed"] == new_task["completed"]

    get_response = client.get(f"/tasks/{create_response.json()['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == new_task["title"]
    assert isinstance(create_response.json()["id"], int)
    assert get_response.json()["completed"] == new_task["completed"]

def test_create_task_invalid_data():
    invalid_task = {
        "title": 123,
        "completed": "not a boolean"
    }

    response = client.post("/tasks/", json=invalid_task)

    assert response.status_code == 422
    assert "detail" in response.json()

def test_update_task():
    task = {
        "title": "Task to update",
        "completed": False
    }

    create_response = client.post("/tasks/", json=task)
    task_id = create_response.json()["id"]

    update_data = {
        "title": "Updated task title",
        "completed": True
    }

    update_response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert create_response.status_code == 201
    assert update_response.status_code == 200
    assert update_response.json()["title"] == update_data["title"]
    assert update_response.json()["completed"] == update_data["completed"]

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == update_data["title"]
    assert get_response.json()["completed"] == update_data["completed"]