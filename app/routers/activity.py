from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityResponse
from app.crud.activity import ActivityCRUD
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/activities",
    tags=["Activities"],
)


@router.get("/", response_model=List[ActivityResponse])
async def get_all_activities(db: Session = Depends(get_db)):
    """
    Получить список всех видов деятельности.

    :param db: Сессия базы данных.
    :return: Список видов деятельности.
    """
    activities = ActivityCRUD.get_all(db)
    return activities


@router.get("/hierarchy", response_model=List[ActivityResponse])
async def get_activities_hierarchy(db: Session = Depends(get_db)):
    """
    Получить иерархический список видов деятельности.

    :param db: Сессия базы данных.
    :return: Иерархический список видов деятельности.
    """
    return ActivityCRUD.get_hierarchy(db)


@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о виде деятельности по его ID.

    :param activity_id: Уникальный идентификатор вида деятельности.
    :param db: Сессия базы данных.
    :return: Вид деятельности.
    """
    activity = ActivityCRUD.get(db, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    return activity


@router.post("/", response_model=ActivityResponse)
async def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """
    Создать новый вид деятельности.

    :param activity: Данные для создания вида деятельности.
    :param db: Сессия базы данных.
    :return: Созданный вид деятельности.
    """
    return ActivityCRUD.create(db, activity)


@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db)):
    """
    Обновить данные вида деятельности.

    :param activity_id: Уникальный идентификатор вида деятельности.
    :param activity: Обновленные данные вида деятельности.
    :param db: Сессия базы данных.
    :return: Обновленный вид деятельности.
    """
    updated_activity = ActivityCRUD.update(db, activity_id, activity)
    if not updated_activity:
        raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    return updated_activity


@router.delete("/{activity_id}", response_model=dict)
async def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Удалить вид деятельности по ID.

    :param activity_id: Уникальный идентификатор вида деятельности.
    :param db: Сессия базы данных.
    :return: Сообщение об успешном удалении.
    """
    if not ActivityCRUD.delete(db, activity_id):
        raise HTTPException(status_code=404, detail="Вид деятельности не найден")
    return {"detail": "Вид деятельности успешно удалён"}