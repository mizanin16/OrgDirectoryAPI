import pytest
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.db import Base
from app.main import app as fastapi_app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.building import Building
from app.models.organization import Organization
from app.models.activity import Activity
from app.core.db import settings

# Настройка тестовой базы данных
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Создание и настройка тестовой БД перед началом тестов.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db():
    """
    Фикстура для создания тестовой сессии базы данных.
    """
    db_session = TestingSessionLocal()
    try:
        yield db_session
        db_session.rollback()
    finally:
        db_session.close()


@pytest.fixture
def client(db: Session):
    """
    Тестовый клиент с заменой зависимости `get_db`.
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.rollback()

    fastapi_app.dependency_overrides[get_db] = override_get_db
    yield TestClient(fastapi_app)
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def test_building_data():
    """
    Тестовые данные для модели Building.
    """
    return {
        "address": "г. Москва, ул. Ленина, 1",
        "latitude": 55.7558,
        "longitude": 37.6173
    }


@pytest.fixture
def test_building(db: Session, test_building_data):
    """
    Создание тестового здания в базе данных.
    """
    building = Building(**test_building_data)
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


@pytest.fixture
def test_organization_data():
    """
    Тестовые данные для модели Organization.
    """
    return {
        "name": "ООО 'Рога и Копыта'",
        "phone_numbers": ["8-800-555-35-35"],
        "building_id": None  # Обновляется динамически
    }


@pytest.fixture
def test_organization(db: Session, test_organization_data, test_building):
    """
    Создание тестовой организации в базе данных.
    """
    test_organization_data["building_id"] = test_building.id
    organization = Organization(**test_organization_data)
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization

@pytest.fixture
def test_activity_data(test_organization):
    """
    Тестовые данные для модели Activity.
    """
    return {
        "name": "Культурное мероприятие",
    }


@pytest.fixture
def test_activity(db: Session, test_activity_data):
    """
    Создание тестовой Activity в базе данных.
    """
    from app.models.activity import Activity

    activity = Activity(**test_activity_data)
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity
