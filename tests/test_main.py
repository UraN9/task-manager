import pytest
from app import main

from fastapi.testclient import TestClient

client = TestClient(main.app)

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
    response = client.get("/tasks/1")
    assert response.json()["id"] == 1
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "id" in response.json()
    assert "title" in response.json()
    assert "completed" in response.json()
    assert isinstance(response.json()["id"], int)
    assert isinstance(response.json()["title"], str)
    assert isinstance(response.json()["completed"], bool)

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}