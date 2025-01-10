import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.core.dependencies import get_db
from app.crud.activity import create_activity_crud, get_activity_crud

client = TestClient(app)


@pytest.fixture
def test_activity_data():
    return {"name": "Test Activity", "parent_id": None}


@pytest.fixture
def test_activity(db: Session, test_activity_data):
    activity = Activity(**test_activity_data)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def test_create_activity(db: Session, test_activity_data):
    response = client.post("/activities/", json=test_activity_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_activity_data["name"]
    assert data["id"] is not None


def test_get_activity(db: Session, test_activity):
    response = client.get(f"/activities/{test_activity.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_activity.id
    assert data["name"] == test_activity.name


def test_update_activity(db: Session, test_activity):
    updated_data = {"name": "Updated Activity", "parent_id": None}
    response = client.put(f"/activities/{test_activity.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Activity"


def test_delete_activity(db: Session, test_activity):
    response = client.delete(f"/activities/{test_activity.id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Activity deleted successfully"}
    assert get_activity_crud(db, test_activity.id) is None
