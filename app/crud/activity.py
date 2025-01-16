from typing import List, Type, Any

from sqlalchemy.orm import Session

from app.models import Activity
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class ActivityCRUD:
    """
    CRUD-класс для работы с сущностью Activity.
    """

    @staticmethod
    def get_all(db: Session) -> list[Type[Activity]]:
        """
        Получить список всех видов деятельности.

        :param db: Сессия базы данных.
        :return: Список всех видов деятельности.
        """
        return db.query(Activity).all()

    @staticmethod
    def get_hierarchy(db: Session) -> list[dict[str, Any]]:
        """
        Получить иерархический список видов деятельности.

        :param db: Сессия базы данных.
        :return: Список видов деятельности с вложенностью.
        """

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

        activities = db.query(Activity).all()
        return build_hierarchy(activities)

    @staticmethod
    def create(db: Session, activity_data: ActivityCreate) -> Activity:
        """
        Создать новый вид деятельности.

        :param db: Сессия базы данных.
        :param activity_data: Данные для создания вида деятельности.
        :return: Созданный вид деятельности.
        """
        new_activity = Activity(**activity_data.model_dump())
        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)
        return new_activity

    @staticmethod
    def get(db: Session, activity_id: int) -> Activity | None:
        """
        Получить вид деятельности по ID.

        :param db: Сессия базы данных.
        :param activity_id: Уникальный идентификатор вида деятельности.
        :return: Вид деятельности или None.
        """
        return db.query(Activity).filter(Activity.id == activity_id).first()

    @staticmethod
    def update(db: Session, activity_id: int, activity_data: ActivityUpdate) -> Type[Activity] | None:
        """
        Обновить данные вида деятельности.

        :param db: Сессия базы данных.
        :param activity_id: Уникальный идентификатор вида деятельности.
        :param activity_data: Обновленные данные вида деятельности.
        :return: Обновленный вид деятельности или None.
        """
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return None
        for key, value in activity_data.model_dump(exclude_unset=True).items():
            setattr(activity, key, value)
        db.commit()
        db.refresh(activity)
        return activity

    @staticmethod
    def delete(db: Session, activity_id: int) -> bool:
        """
        Удалить вид деятельности по ID.

        :param db: Сессия базы данных.
        :param activity_id: Уникальный идентификатор вида деятельности.
        :return: True, если вид деятельности удалён, иначе False.
        """
        activity = db.query(Activity).filter(Activity.id == activity_id).first()
        if not activity:
            return False
        db.delete(activity)
        db.commit()
        return True