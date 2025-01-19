from loguru import logger
from sqlalchemy.orm import Session
from typing import List
from app.models.activity import Activity
from .base import BaseCRUD


class ActivityCRUD(BaseCRUD[Activity]):
    def __init__(self):
        super().__init__(Activity)

    def get_hierarchy(self, db: Session) -> List[dict]:
        logger.info("Получение иерархии для модели {model}", model=self.model.__name__)

        def build_hierarchy(activities, parent_id=None):
            return [
                {
                    "id": activity.id,
                    "name": activity.name,
                    "parent_id": activity.parent_id,
                    "children": build_hierarchy(activities, activity.id),
                }
                for activity in activities if activity.parent_id == parent_id
            ]

        activities = db.query(self.model).all()
        return build_hierarchy(activities)
