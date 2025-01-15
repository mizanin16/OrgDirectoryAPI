from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.crud.building import BuildingCRUD
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
)


@router.get("/", response_model=List[BuildingResponse])
async def get_all_buildings(db: Session = Depends(get_db)):
    """
    Получить список всех зданий.

    :param db: Сессия базы данных.
    :return: Список зданий.
    """
    buildings = BuildingCRUD.get_all(db)
    return buildings


@router.post("/", response_model=BuildingResponse)
async def create_building(building: BuildingCreate, db: Session = Depends(get_db)):
    """
    Создать новое здание.

    :param building: Данные для создания здания.
    :param db: Сессия базы данных.
    :return: Созданное здание.
    """
    return BuildingCRUD.create(db, building)


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(building_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о здании по его ID.

    :param building_id: Уникальный идентификатор здания.
    :param db: Сессия базы данных.
    :return: Информация о здании.
    """
    building = BuildingCRUD.get(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Здание не найдено")
    return building


@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(building_id: int, building: BuildingUpdate, db: Session = Depends(get_db)):
    """
    Обновить данные здания.

    :param building_id: Уникальный идентификатор здания.
    :param building: Обновленные данные здания.
    :param db: Сессия базы данных.
    :return: Обновленное здание.
    """
    updated_building = BuildingCRUD.update(db, building_id, building)
    if not updated_building:
        raise HTTPException(status_code=404, detail="Здание не найдено")
    return updated_building


@router.delete("/{building_id}", response_model=dict)
async def delete_building(building_id: int, db: Session = Depends(get_db)):
    """
    Удалить здание по ID.

    :param building_id: Уникальный идентификатор здания.
    :param db: Сессия базы данных.
    :return: Сообщение об успешном удалении.
    """
    if not BuildingCRUD.delete(db, building_id):
        raise HTTPException(status_code=404, detail="Здание не найдено")
    return {"detail": "Здание успешно удалено"}