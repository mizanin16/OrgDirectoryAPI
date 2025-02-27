from loguru import logger
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import or_
from typing import List, Type
from app.models.organization import Organization
from app.models.activity import Activity
from .base import BaseCRUD


class OrganizationCRUD(BaseCRUD[Organization]):
    def __init__(self):
        super().__init__(Organization)

    def search_by_name(self, db: Session, name: str) -> list[Type[Organization]]:
        logger.info("Поиск организаций по имени: {name}", name=name)
        return db.query(self.model).filter(self.model.name.ilike(f"%{name}%")).all()

    def get_organizations_by_activity(self, db: Session, activity_id: int) -> List[Type[Organization]]:
        logger.info("Получение организаций по виду деятельности ID: {activity_id}", activity_id=activity_id)

        # Создаем алиас для самоссылающейся таблицы
        # Явно указать связь между родительскими и дочерними элементами таблицы activities
        child_activities = aliased(Activity)

        # Получаем ID всех связанных дочерних деятельностей
        child_ids = (
            db.query(Activity.id)
            .join(child_activities, child_activities.parent_id == Activity.id, isouter=True)
            .filter(or_(Activity.id == activity_id, child_activities.parent_id == activity_id))
            .all()
        )

        # Извлекаем ID для фильтрации
        child_ids = [item[0] for item in child_ids]

        return (
            db.query(self.model)
            .join(self.model.activities)  # Присоединяем таблицу activities через связь
            .filter(Activity.id.in_(child_ids))  # Фильтруем по ID родителя и детей
            .all()
        )
