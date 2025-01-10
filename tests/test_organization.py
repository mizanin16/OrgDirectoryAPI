import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.models.organization import Organization
from app.models.building import Building
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.core.dependencies import get_db
from app.crud.organization import create_organization_crud, get_organization_crud

client = TestClient(app)


@pytest.fixture
def test_building(db: Session):
    building = Building(address="Test Address")  # Создайте тестовое здание
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


@pytest.fixture
def test_organization_data(test_building):  # Используем фикстуру test_building
    return {
        "name": "Test Organization",
        "phone_numbers": ["+123456789", "+987654321"],
        "building_id": test_building.id,  # Используем id созданного здания
    }


@pytest.fixture
def test_organization(db: Session, test_organization_data):
    organization = Organization(**test_organization_data)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def test_create_organization(db: Session, test_organization_data):
    response = client.post("/organizations/", json=test_organization_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_organization_data["name"]
    assert data["phone_numbers"] == test_organization_data["phone_numbers"]
    assert data["building_id"] == test_organization_data["building_id"]
    assert data["id"] is not None


def test_get_organization(db: Session, test_organization):
    response = client.get(f"/organizations/{test_organization.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_organization.id
    assert data["name"] == test_organization.name
    assert data["phone_numbers"] == test_organization.phone_numbers
    assert data["building_id"] == test_organization.building_id


def test_update_organization(db: Session, test_organization):
    updated_data = {
        "name": "Updated Organization",
        "phone_numbers": ["+111111111"],
        "building_id": 2,
    }
    response = client.put(f"/organizations/{test_organization.id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Organization"
    assert data["phone_numbers"] == ["+111111111"]
    assert data["building_id"] == 2


def test_delete_organization(db: Session, test_organization):
    response = client.delete(f"/organizations/{test_organization.id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Organization deleted successfully"}
    assert get_organization_crud(db, test_organization.id) is None
