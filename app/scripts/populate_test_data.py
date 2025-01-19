from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.building import Building
from app.models.organization import Organization
from app.models.activity import Activity
from faker import Faker
import random

# Указываем локальность для генерации русских данных
fake = Faker('ru_RU')

def seed_data(db: Session, num_buildings: int, num_activities: int, num_organizations: int):
    # Генерация зданий
    buildings = [
        Building(
            address=fake.address(),
            latitude=fake.latitude(),
            longitude=fake.longitude()
        ) for _ in range(num_buildings)
    ]
    db.add_all(buildings)
    db.commit()

    # Генерация видов деятельности
    activities = [
        Activity(name=fake.word()) for _ in range(num_activities)
    ]
    db.add_all(activities)
    db.commit()

    # Генерация организаций
    organizations = [
        Organization(
            name=fake.company(),
            phone_numbers=[fake.phone_number() for _ in range(random.randint(1, 3))],
            building_id=random.choice(buildings).id  # Привязываем к случайному зданию
        ) for _ in range(num_organizations)
    ]
    db.add_all(organizations)
    db.commit()

    # Привязываем виды деятельности к организациям
    for org in organizations:
        # Привязываем случайные виды деятельности к организации
        assigned_activities = random.sample(activities, k=random.randint(1, len(activities)))
        org.activities.extend(assigned_activities)

    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try:
        num_buildings = 5  # Задайте количество зданий
        num_activities = 10  # Задайте количество видов деятельности
        num_organizations = 15  # Задайте количество организаций

        seed_data(db, num_buildings, num_activities, num_organizations)
        print("База данных успешно заполнена тестовыми данными!")
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
    finally:
        db.close()