from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.crud.organization import OrganizationCRUD
from app.core.dependencies import get_db

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.get("/", response_model=List[OrganizationResponse])
async def get_all_organizations(
        db: Session = Depends(get_db),
        name: Optional[str] = Query(None, description="Фильтрация по названию организации"),
        activity_id: Optional[int] = Query(None, description="Фильтрация по ID вида деятельности"),
        latitude: Optional[float] = Query(None, description="Широта для фильтрации по радиусу"),
        longitude: Optional[float] = Query(None, description="Долгота для фильтрации по радиусу"),
        radius: Optional[float] = Query(None, description="Радиус поиска в километрах"),
):
    """
    Получить список всех организаций с возможностью фильтрации.

    :param db: Сессия базы данных.
    :param name: Название организации для фильтрации.
    :param activity_id: ID вида деятельности для фильтрации.
    :param latitude: Широта для поиска организаций в радиусе.
    :param longitude: Долгота для поиска организаций в радиусе.
    :param radius: Радиус поиска в километрах.
    :return: Список организаций.
    """
    return OrganizationCRUD.get_filtered(db, name, activity_id, latitude, longitude, radius)


@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(organization_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию об организации по её ID.

    :param organization_id: Уникальный идентификатор организации.
    :param db: Сессия базы данных.
    :return: Организация.
    """
    organization = OrganizationCRUD.get(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return organization


@router.post("/", response_model=OrganizationResponse)
async def create_organization(organization: OrganizationCreate, db: Session = Depends(get_db)):
    """
    Создать новую организацию.

    :param organization: Данные для создания организации.
    :param db: Сессия базы данных.
    :return: Созданная организация.
    """
    return OrganizationCRUD.create(db, organization)


@router.put("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(organization_id: int, organization: OrganizationUpdate, db: Session = Depends(get_db)):
    """
    Обновить данные организации.

    :param organization_id: Уникальный идентификатор организации.
    :param organization: Обновленные данные организации.
    :param db: Сессия базы данных.
    :return: Обновленная организация.
    """
    updated_organization = OrganizationCRUD.update(db, organization_id, organization)
    if not updated_organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return updated_organization


@router.delete("/{organization_id}", response_model=dict)
async def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    """
    Удалить организацию по ID.

    :param organization_id: Уникальный идентификатор организации.
    :param db: Сессия базы данных.
    :return: Сообщение об успешном удалении.
    """
    if not OrganizationCRUD.delete(db, organization_id):
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return {"detail": "Организация успешно удалена"}