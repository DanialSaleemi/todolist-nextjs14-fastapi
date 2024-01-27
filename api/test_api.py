from fastapi.testclient import TestClient
from fastapi import status
from .index import app

client = TestClient(app=app)

def test_get_all_todos():
    response = client.get("/api/todos")
    assert response.status_code == status.HTTP_200_OK


def test_get_todo_item():
    response = client.get("api/todos/", params={"item_id": 3})
    assert response.status_code == status.HTTP_200_OK

def test_post_todo_item():
    response = client.post("api/todos/", json={"title": "test"})
    assert response.status_code == status.HTTP_201_CREATED