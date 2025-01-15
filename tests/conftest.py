import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.dependencies import get_db
from app.core.db import Base
from app.main import app as fastapi_app
from app.core.db import settings

# Импорты для тестовых данных
from app.models.building import Building
from app.models.organization import Organization
from app.models.activity import Activity

TEST_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_test_data(db):
    """Заполнение БД тестовыми данными"""
    # Здания
    buildings = [
        Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173),
        Building(address="г. Санкт-Петербург, ул. Блюхера 32/1", latitude=59.9343, longitude=30.3351),
        Building(address="г. Новосибирск, пр. Дзержинского, 10", latitude=55.0302, longitude=82.9204),
    ]
    db.add_all(buildings)
    db.commit()

    # Виды деятельности
    activities = [
        Activity(name="Еда"),
        Activity(name="Мясная продукция"),
        Activity(name="Молочная продукция"),
        Activity(name="Автомобили"),
        Activity(name="Грузовые"),
        Activity(name="Легковые"),
    ]
    db.add_all(activities)
    db.commit()

    # Установка parent_id после создания
    activities[1].parent_id = activities[0].id  # Мясная продукция -> Еда
    activities[2].parent_id = activities[0].id  # Молочная продукция -> Еда
    activities[4].parent_id = activities[3].id  # Грузовые -> Автомобили
    activities[5].parent_id = activities[3].id  # Легковые -> Автомобили
    db.commit()

    # Организации
    organizations = [
        Organization(
            name="ООО 'Рога и Копыта'",
            phone_numbers=["2-222-222", "3-333-333"],
            building_id=buildings[1].id,
        ),
        Organization(
            name="Магазин 'Молочные продукты'",
            phone_numbers=["8-800-555-35-35"],
            building_id=buildings[0].id,
        ),
    ]
    db.add_all(organizations)
    db.commit()

    # Связи организаций с видами деятельности
    activities[1].organizations.append(organizations[0])  # Мясная продукция -> Рога и Копыта
    activities[2].organizations.append(organizations[1])  # Молочная продукция -> Молочные продукты
    db.commit()

    return {
        "buildings": buildings,
        "activities": activities,
        "organizations": organizations
    }


@pytest.fixture(scope="session")
def setup_test_db():
    """Создание и настройка тестовой БД"""
    # Удаляем все таблицы перед тестами
    Base.metadata.drop_all(bind=engine)
    # Создаем все таблицы заново
    Base.metadata.create_all(bind=engine)

    # Создаем сессию
    db = TestingSessionLocal()
    try:
        # Создаем тестовые данные
        test_data = seed_test_data(db)
        yield test_data
    finally:
        db.close()
        # Удаляем все таблицы после тестов
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_db():
    """Фикстура для доступа к тестовой БД"""
    db = TestingSessionLocal()
    try:
        yield db
        # Откатываем изменения после каждого теста
        db.rollback()
    finally:
        db.close()

@pytest.fixture
def client(test_db, test_data):
    """Тестовый клиент с настроенной БД"""
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.rollback()  # Откатываем изменения после каждого запроса

    fastapi_app.dependency_overrides[get_db] = override_get_db
    yield TestClient(fastapi_app)
    fastapi_app.dependency_overrides.clear()

@pytest.fixture
def test_data(test_db):
    """Фикстура для доступа к тестовым данным"""
    data = seed_test_data(test_db)
    test_db.commit()
    return data

@pytest.fixture(autouse=True)
def cleanup(test_db):
    yield
    test_db.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        test_db.execute(table.delete())
    test_db.commit()