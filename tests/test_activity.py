import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.core.dependencies import get_db
from app.crud.activity import ActivityCRUD

client = TestClient(app)


def test_create_activity(client: TestClient, test_activity_data):
    response = client.post("/activities/", json=test_activity_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_activity_data["name"]


def test_get_activity(client: TestClient, test_activity):
    response = client.get(f"/activities/{test_activity.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_activity.id
    assert data["name"] == test_activity.name


def test_update_activity(client: TestClient, test_activity):
    updated_data = {
        "name": "Обновленное мероприятие",
    }
    response = client.put(f"/activities/{test_activity.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]


def test_delete_activity(client: TestClient, test_activity):
    response = client.delete(f"/activities/{test_activity.id}")
    assert response.status_code == 200
    assert response.json() == {"message": 'Item deleted successfully'}
