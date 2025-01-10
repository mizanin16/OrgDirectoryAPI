from app.models.building import Building
from app.models.organization import Organization
from sqlalchemy.orm import sessionmaker
from app.core.db import engine

Session = sessionmaker(bind=engine)
session = Session()

try:
    # Добавляем запись в таблицу buildings
    new_building = Building(
        address="123 Test St",
        latitude=40.7128,
        longitude=-74.0060
    )
    session.add(new_building)
    session.commit()  # Зафиксировать, чтобы получить ID нового здания

    # Используем ID нового здания для организации
    new_organization = Organization(
        name="Test Organization",
        phone_numbers=["+123456789"],
        building_id=None  # building_id не указывается
    )
    session.add(new_organization)
    session.commit()
    print("Organization added successfully!")
except Exception as e:
    session.rollback()
    print(f"Error occurred: {e}")
finally:
    session.close()
