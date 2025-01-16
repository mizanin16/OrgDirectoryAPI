from typing import List, Optional, Type

from sqlalchemy.orm import Session

from app.models import Organization
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from geopy.distance import geodesic


class OrganizationCRUD:
    """
    CRUD-класс для работы с сущностью Organization.
    """

    @staticmethod
    def get_filtered(
            db: Session,
            name: Optional[str] = None,
            activity_id: Optional[int] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            radius: Optional[float] = None,
    ) -> list[Type[Organization]]:
        """
        Получить список организаций с фильтрацией.

        :param db: Сессия базы данных.
        :param name: Название организации.
        :param activity_id: ID вида деятельности.
        :param latitude: Широта для поиска.
        :param longitude: Долгота для поиска.
        :param radius: Радиус поиска.
        :return: Список организаций.
        """
        query = db.query(Organization)
        if name:
            query = query.filter(Organization.name.ilike(f"%{name}%"))
        if activity_id:
            query = query.filter(Organization.activity_id == activity_id)
        if latitude and longitude and radius:
            organizations = query.all()
            return [org for org in organizations if
                geodesic((latitude, longitude), (org.building.latitude, org.building.longitude)).km <= radius
            ]
        return query.all()

    @staticmethod
    def get(db: Session, organization_id: int) -> Organization | None:
        """
        Получить организацию по ID.

        :param db: Сессия базы данных.
        :param organization_id: Уникальный идентификатор организации.
        :return: Организация или None.
        """
        return db.query(Organization).filter(Organization.id == organization_id).first()

    @staticmethod
    def create(db: Session, organization_data: OrganizationCreate) -> Organization:
        """
        Создать новую организацию.

        :param db: Сессия базы данных.
        :param organization_data: Данные для создания организации.
        :return: Созданная организация.
        """
        new_organization = Organization(**organization_data.model_dump())
        db.add(new_organization)
        db.commit()
        db.refresh(new_organization)
        return new_organization

    @staticmethod
    def update(db: Session, organization_id: int, organization_data: OrganizationUpdate) -> Type[Organization] | None:
        """
        Обновить данные организации.

        :param db: Сессия базы данных.
        :param organization_id: Уникальный идентификатор организации.
        :param organization_data: Обновленные данные организации.
        :return: Обновленная организация или None.
        """
        organization = db.query(Organization).filter(Organization.id == organization_id).first()
        if not organization:
            return None
        for key, value in organization_data.model_dump(exclude_unset=True).items():
            setattr(organization, key, value)
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def delete(db: Session, organization_id: int) -> bool:
        """
        Удалить организацию по ID.

        :param db: Сессия базы данных.
        :param organization_id: Уникальный идентификатор организации.
        :return: True, если организация удалена, иначе False.
        """
        organization = db.query(Organization).filter(Organization.id == organization_id).first()
        if not organization:
            return False
        db.delete(organization)
        db.commit()
        return True
