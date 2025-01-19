from loguru import logger
from sqlalchemy.orm import Session
from typing import Type, TypeVar, Generic, List

T = TypeVar("T")


class BaseCRUD(Generic[T]):
    """
    Базовый CRUD-класс для работы с сущностями.
    """

    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self, db: Session) -> List[T]:
        logger.info("Получение всех записей модели {model}", model=self.model.__name__)
        return db.query(self.model).all()

    def get(self, db: Session, obj_id: int) -> T | None:
        logger.info("Получение записи модели {model} по ID: {id}", model=self.model.__name__, id=obj_id)
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def create(self, db: Session, obj_data: dict) -> T:
        logger.info("Создание записи модели {model} с данными: {data}", model=self.model.__name__, data=obj_data)
        new_obj = self.model(**obj_data)
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)
        return new_obj

    def update(self, db: Session, obj_id: int, obj_data: dict) -> T | None:
        logger.info("Обновление записи модели {model} с ID: {id}, данные: {data}", model=self.model.__name__, id=obj_id, data=obj_data)
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            logger.warning("Запись модели {model} с ID {id} не найдена", model=self.model.__name__, id=obj_id)
            return None
        for key, value in obj_data.items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, obj_id: int) -> bool:
        logger.info("Удаление записи модели {model} с ID: {id}", model=self.model.__name__, id=obj_id)
        obj = db.query(self.model).filter(self.model.id == obj_id).first()
        if not obj:
            logger.warning("Запись модели {model} с ID {id} не найдена для удаления", model=self.model.__name__, id=obj_id)
            return False
        db.delete(obj)
        db.commit()
        return True
