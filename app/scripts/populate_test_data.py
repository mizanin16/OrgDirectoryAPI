from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models.building import Building
from app.models.organization import Organization
from app.models.activity import Activity


def seed_data(db: Session):
    # Добавляем здания
    buildings = [
        Building(address="г. Москва, ул. Ленина 1, офис 3", latitude=55.7558, longitude=37.6173),
        Building(address="г. Санкт-Петербург, ул. Блюхера 32/1", latitude=59.9343, longitude=30.3351),
        Building(address="г. Новосибирск, пр. Дзержинского, 10", latitude=55.0302, longitude=82.9204),
    ]
    db.add_all(buildings)
    db.commit()
    # todo: сделать чтобы добавление в БД происходило без конкретного указания id parent, а указать просто имя
    # Добавляем виды деятельности (древовидная структура)
    activities = [
        Activity(name="Еда"),
        Activity(name="Мясная продукция", parent_id=1),
        Activity(name="Молочная продукция", parent_id=1),
        Activity(name="Автомобили"),
        Activity(name="Грузовые", parent_id=4),
        Activity(name="Легковые", parent_id=4),
        Activity(name="Запчасти", parent_id=6),
        Activity(name="Аксессуары", parent_id=6),
    ]
    db.add_all(activities)
    db.commit()

    # Добавляем организации
    organizations = [
        Organization(
            name="ООО 'Рога и Копыта'",
            phone_numbers=["2-222-222", "3-333-333", "8-923-666-13-13"],
            building_id=buildings[1].id,
        ),
        Organization(
            name="Магазин 'Молочные продукты'",
            phone_numbers=["8-800-555-35-35"],
            building_id=buildings[0].id,
        ),
        Organization(
            name="Автосервис 'Грузовичок'",
            phone_numbers=["8-800-777-88-88"],
            building_id=buildings[2].id,
        ),
    ]
    db.add_all(organizations)
    db.commit()

    # Привязываем виды деятельности к организациям
    activities[1].organizations.append(organizations[0])  # Мясная продукция -> ООО 'Рога и Копыта'
    activities[2].organizations.append(organizations[1])  # Молочная продукция -> Магазин 'Молочные продукты'
    activities[4].organizations.append(organizations[2])  # Грузовые -> Автосервис 'Грузовичок'
    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
        print("База данных успешно заполнена тестовыми данными!")
    except Exception as e:
        print(f"Ошибка при заполнении базы данных: {e}")
    finally:
        db.close()
