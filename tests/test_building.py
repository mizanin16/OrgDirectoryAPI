import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.core.db import Base, engine
from app.schemas.building import BuildingCreate
from app.models.building import Building

client = TestClient(app)

def test_create_building(client: TestClient, test_building_data):
    """
    Тест на создание объекта Building через API.
    """
    response = client.post("/buildings/", json=test_building_data)
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == test_building_data["address"]
    assert data["latitude"] == test_building_data["latitude"]
    assert data["longitude"] == test_building_data["longitude"]


def test_get_building(client: TestClient, test_building):
    """
    Тест на получение объекта Building через API.
    """
    response = client.get(f"/buildings/{test_building.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_building.id
    assert data["address"] == test_building.address


def test_update_building(client: TestClient, test_building):
    """
    Тест на обновление объекта Building через API.
    """
    updated_data = {
        "address": "г. Санкт-Петербург, ул. Пушкина, д. 10",
        "latitude": 59.9343,
        "longitude": 30.3351
    }
    response = client.put(f"/buildings/{test_building.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["address"] == updated_data["address"]
    assert data["latitude"] == updated_data["latitude"]
    assert data["longitude"] == updated_data["longitude"]


def test_delete_building(client: TestClient, test_building):
    response = client.delete(f"/buildings/{test_building.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}  # Исправлено под локализацию
