from typing import Type

from sqlalchemy.orm import Session
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate


class BuildingCRUD:
    """
    CRUD-класс для работы с сущностью Building.
    """

    @staticmethod
    def get_all(db: Session):
        """
        Получить список всех зданий.

        :param db: Сессия базы данных.
        :return: Список всех зданий.
        """
        return db.query(Building).all()

    @staticmethod
    def create(db: Session, building_data: BuildingCreate) -> Building:
        """
        Создать новое здание.

        :param db: Сессия базы данных.
        :param building_data: Данные для создания здания.
        :return: Созданное здание.
        """
        new_building = Building(**building_data.dict())
        db.add(new_building)
        db.commit()
        db.refresh(new_building)
        return new_building

    @staticmethod
    def get(db: Session, building_id: int) -> Building | None:
        """
        Получить здание по ID.

        :param db: Сессия базы данных.
        :param building_id: Уникальный идентификатор здания.
        :return: Здание или None.
        """
        return db.query(Building).filter(Building.id == building_id).first()

    @staticmethod
    def update(db: Session, building_id: int, building_data: BuildingUpdate) -> Type[Building] | None:
        """
        Обновить данные здания.

        :param db: Сессия базы данных.
        :param building_id: Уникальный идентификатор здания.
        :param building_data: Обновленные данные здания.
        :return: Обновленное здание или None.
        """
        building = db.query(Building).filter(Building.id == building_id).first()
        if not building:
            return None
        for key, value in building_data.dict(exclude_unset=True).items():
            setattr(building, key, value)
        db.commit()
        db.refresh(building)
        return building

    @staticmethod
    def delete(db: Session, building_id: int) -> bool:
        """
        Удалить здание по ID.

        :param db: Сессия базы данных.
        :param building_id: Уникальный идентификатор здания.
        :return: True, если здание удалено, иначе False.
        """
        building = db.query(Building).filter(Building.id == building_id).first()
        if not building:
            return False
        db.delete(building)
        db.commit()
        return True
