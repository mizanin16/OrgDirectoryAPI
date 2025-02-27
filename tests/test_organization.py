import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.organization import Organization
from app.models.building import Building
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.core.dependencies import get_db
from app.crud.organization import OrganizationCRUD

client = TestClient(app)

def test_create_organization(client: TestClient, test_organization_data, test_building):
    """
    Тест на создание объекта Organization через API.
    """
    test_organization_data["building_id"] = test_building.id
    response = client.post("/organizations/", json=test_organization_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_organization_data["name"]
    assert data["phone_numbers"] == test_organization_data["phone_numbers"]


def test_get_organization(client: TestClient, test_organization):
    """
    Тест на получение объекта Organization через API.
    """
    response = client.get(f"/organizations/{test_organization.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_organization.id
    assert data["name"] == test_organization.name


def test_update_organization(client: TestClient, test_organization):
    """
    Тест на обновление объекта Organization через API.
    """
    updated_data = {
        "name": "ООО 'Новое Название'",
        "phone_numbers": ["+7-800-555-66-77"]
    }
    response = client.put(f"/organizations/{test_organization.id}", json=updated_data)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["phone_numbers"] == updated_data["phone_numbers"]


def test_delete_organization(client: TestClient, test_organization):
    response = client.delete(f"/organizations/{test_organization.id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}  # Исправлено под локализацию
