import pytest
import main

from fastapi.testclient import TestClient

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def reset_tasks(monkeypatch):
    monkeypatch.setattr(main, "tasks", [
        {"id": 1, "title": "Learn FastAPI", "completed": False},
        {"id": 2, "title": "Practice SQL", "completed": True},
    ])


def test_main_route():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API"}

def test_about_route():
    response = client.get("/about")

    assert response.status_code == 200
    assert response.json() == {"name": "Task Manager", "version": "1.0.0"}

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2

def test_get_tasks_by_id():
    response = client.get("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Learn FastAPI", "completed": False}

def test_get_filtered_tasks_by_completed():
    response = client.get("/tasks?completed=true")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["completed"] is True

def test_get_filtered_tasks_by_title():
    response = client.get("/tasks?title=learn")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert "learn" in response.json()[0]["title"].lower()


def test_post_tasks():
    responce = client.post("/tasks", json={"title": "New Task", "completed": True})

    assert responce.status_code == 201
    assert responce.json()["title"] == "New Task"
    assert responce.json()["completed"] is True
    assert "id" in responce.json()

def test_post_tasks_missing_title():
    response = client.post(
        "/tasks",
        json={"completed": True}
    )

    assert response.status_code == 422

def test_patch_tasks():
    responce = client.patch("/tasks/1", json={"title": "Updated Task", "completed": True})

    assert responce.status_code == 200
    assert responce.json()["title"] == "Updated Task"
    assert responce.json()["completed"] is True

def test_patch_tasks_partial_update():
    response = client.patch(
        "/tasks/1",
        json={"title": "Updated Task"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["completed"] is False

def test_patch_tasks_empty_data():
    response = client.patch("/tasks/1", json={})

    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"
    assert response.json()["completed"] is False

def test_patch_tasks_not_found():
    responce = client.patch("/tasks/999", json={"title": "Updated Task", "completed": True})

    assert responce.status_code == 404

def test_get_tasks_by_id_not_found():
    response = client.get("/tasks/999")

    assert response.status_code == 404

def test_post_tasks_invalid_data():
    responce = client.post("/tasks", json={"title": 123, "completed": "not_a_boolean"})

    assert responce.status_code == 422

def test_delete_tasks():
    responce = client.delete("/tasks/1")

    assert responce.status_code == 204

def test_delete_tasks_not_found():
    responce = client.delete("/tasks/999")

    assert responce.status_code == 404