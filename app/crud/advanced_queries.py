from sqlalchemy.orm import Session
from app.models import Building
from app.models.organization import Organization
from app.models.building import Building
from app.models.activity import Activity
from typing import List, Type
from math import radians, cos, sin, sqrt, atan2


class AdvancedQueryCRUD:
    """
    CRUD-класс для сложных запросов.
    """

    @staticmethod
    def get_organizations_by_activity(db: Session, activity_id: int, max_depth: int) -> List[Organization]:
        """
        Получает организации, связанные с видом деятельности (с учетом вложенности).

        :param db: Сессия базы данных.
        :param activity_id: ID вида деятельности.
        :param max_depth: Максимальный уровень вложенности.
        :return: Список организаций.
        """
        result = []
        visited = set()

        def traverse(activity_id, depth):
            if depth > max_depth or activity_id in visited:
                return
            visited.add(activity_id)
            activity = db.query(Activity).filter(Activity.id == activity_id).first()
            if not activity:
                return
            result.extend(activity.organizations)
            for child in activity.children:
                traverse(child.id, depth + 1)

        traverse(activity_id, 0)
        return result

    @staticmethod
    def get_buildings_in_radius(db: Session, latitude: float, longitude: float, radius: float) -> list[Type[Building]]:
        """
        Получает здания в радиусе от указанной точки.

        :param db: Сессия базы данных.
        :param latitude: Широта точки.
        :param longitude: Долгота точки.
        :param radius: Радиус поиска в километрах.
        :return: Список зданий.
        """

        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Радиус Земли в километрах
            dlat = radians(lat2 - lat1)
            dlon = radians(lon2 - lon1)
            a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
            return 2 * R * atan2(sqrt(a), sqrt(1 - a))

        buildings = db.query(Building).all()
        return [building for building in buildings if
                haversine(latitude, longitude, building.latitude, building.longitude) <= radius
                ]

    @staticmethod
    def search_organizations_by_name(db: Session, name: str) -> list[Type[Organization]]:
        """
        Поиск организаций по названию.

        :param db: Сессия базы данных.
        :param name: Название организации.
        :return: Список организаций.
        """
        return db.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()
