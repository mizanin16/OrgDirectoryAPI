from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.routers.base_router import BaseRouter
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.crud.building import BuildingCRUD
from app.core.dependencies import get_db

router = APIRouter()

building_crud = BuildingCRUD()

@router.get("/buildings/", response_model=List[BuildingResponse], tags=["buildings"])
def get_buildings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Получение списка зданий с пагинацией"""
    buildings = (
        db.query(Building)
        .options(
            joinedload(Building.organizations)
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    def build_building_response(building):
        # Преобразуем организации в список ID
        org_ids = [org.id for org in building.organizations] if building.organizations else []

        return BuildingResponse(
            id=building.id,
            address=building.address,
            latitude=building.latitude,
            longitude=building.longitude,
            organizations=org_ids,
            organizations_count=len(org_ids)
        )

    return [build_building_response(building) for building in buildings]


@router.get("/buildings/{item_id}", response_model=BuildingResponse, tags=["buildings"])
def get_building(item_id: int, db: Session = Depends(get_db)):
    """Получение здания по ID"""
    building = (
        db.query(Building)
        .options(
            joinedload(Building.organizations)
        )
        .filter(Building.id == item_id)
        .first()
    )

    if not building:
        raise HTTPException(status_code=404, detail="Building not found")

    # Преобразуем организации в список ID
    org_ids = [org.id for org in building.organizations] if building.organizations else []

    return BuildingResponse(
        id=building.id,
        address=building.address,
        latitude=building.latitude,
        longitude=building.longitude,
        organizations=org_ids,
        organizations_count=len(org_ids)
    )


@router.get("/radius", response_model=List[BuildingResponse], tags=["buildings"])
def get_buildings_in_radius(latitude: float, longitude: float, radius: float, db: Session = Depends(get_db)):
    """Получение зданий в радиусе"""
    return building_crud.get_buildings_in_radius(db, latitude, longitude, radius)


building_router = BaseRouter(
    model=Building,
    schema_create=BuildingCreate,
    schema_update=BuildingUpdate,
    schema_response=BuildingResponse,
)

router.include_router(building_router.router, prefix="/buildings", tags=["buildings"])