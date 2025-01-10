import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.db import Base, engine
from app.schemas.building import BuildingCreate
from app.models.building import Building

client = TestClient(app)


@pytest.fixture
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_building(setup_db, db: Session):
    data = {
        "address": "123 Main St",
        "latitude": 45.0,
        "longitude": -93.0,
    }
    response = client.post("/buildings/", json=data)
    assert response.status_code == 200
    assert response.json()["address"] == "123 Main St"
    assert response.json()["latitude"] == 45.0
    assert response.json()["longitude"] == -93.0


def test_get_buildings(setup_db, db: Session):
    building = Building(address="Test St", latitude=40.0, longitude=-90.0)
    db.add(building)
    db.commit()

    response = client.get("/buildings/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_update_building(setup_db, db: Session):
    building = Building(address="Old St", latitude=40.0, longitude=-90.0)
    db.add(building)
    db.commit()
    db.refresh(building)

    data = {
        "address": "New St"
    }
    response = client.put(f"/buildings/{building.id}", json=data)
    assert response.status_code == 200
    assert response.json()["address"] == "New St"


def test_delete_building(setup_db, db: Session):
    building = Building(address="Delete St", latitude=40.0, longitude=-90.0)
    db.add(building)
    db.commit()
    db.refresh(building)

    response = client.delete(f"/buildings/{building.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Building deleted successfully"
