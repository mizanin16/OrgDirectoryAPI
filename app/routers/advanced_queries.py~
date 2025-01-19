from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.organization import OrganizationResponse
from app.schemas.building import BuildingResponse
from app.crud.advanced_queries import AdvancedQueryCRUD
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/queries",
    tags=["Advanced Queries"],
)


@router.get("/organizations/activity/{activity_id}", response_model=List[OrganizationResponse])
async def get_organizations_by_activity(
        activity_id: int,
        max_depth: int = 3,
        db: Session = Depends(get_db),
):
    """
    Возвращает список организаций, связанных с указанным видом деятельности (с учетом вложенности).

    :param activity_id: Уникальный идентификатор вида деятельности.
    :param max_depth: Максимальный уровень вложенности (по умолчанию 3).
    :param db: Сессия базы данных.
    :return: Список организаций.
    """
    organizations = AdvancedQueryCRUD.get_organizations_by_activity(db, activity_id, max_depth)
    if not organizations:
        raise HTTPException(status_code=404, detail="Организации не найдены")
    return organizations


@router.get("/buildings/radius", response_model=List[BuildingResponse])
async def get_buildings_in_radius(
        latitude: float,
        longitude: float,
        radius: float,
        db: Session = Depends(get_db),
):
    """
    Возвращает список зданий, находящихся в указанном радиусе от заданной точки.

    :param latitude: Широта точки на карте.
    :param longitude: Долгота точки на карте.
    :param radius: Радиус поиска в километрах.
    :param db: Сессия базы данных.
    :return: Список зданий.
    """
    buildings = AdvancedQueryCRUD.get_buildings_in_radius(db, latitude, longitude, radius)
    if not buildings:
        raise HTTPException(status_code=404, detail="Здания не найдены")
    return buildings


@router.get("/organizations/search", response_model=List[OrganizationResponse])
async def search_organizations_by_name(
        name: str,
        db: Session = Depends(get_db),
):
    """
    Поиск организаций по названию.

    :param name: Название или часть названия организации.
    :param db: Сессия базы данных.
    :return: Список найденных организаций.
    """
    organizations = AdvancedQueryCRUD.search_organizations_by_name(db, name)
    if not organizations:
        raise HTTPException(status_code=404, detail="Организации не найдены")
    return organizations
