from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.crud.building import (
    create_building_crud,
    update_building_crud,
    delete_building_crud,
    get_all_buildings_crud,
    get_building_crud
)
from app.core.dependencies import get_db
from typing import Optional

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=list[BuildingResponse])
def get_buildings(
        skip: int = 0,
        limit: int = 10,
        has_organizations: Optional[bool] = None,
        sort_by: Optional[str] = None,
        db: Session = Depends(get_db),
):
    buildings = get_all_buildings_crud(db, skip, limit)
    if has_organizations is not None:
        buildings = [
            b for b in buildings if bool(b.organizations) == has_organizations
        ]
    if sort_by:
        if sort_by == "address":
            buildings = sorted(buildings, key=lambda x: x.address)
    return buildings


@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(building_id: int, db: Session = Depends(get_db)):
    building = get_building_crud(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.post("/", response_model=BuildingResponse)
def create_building(building_data: BuildingCreate, db: Session = Depends(get_db)):
    return create_building_crud(db, building_data)


@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(building_id: int, building_data: BuildingUpdate, db: Session = Depends(get_db)):
    building = update_building_crud(db, building_id, building_data)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.delete("/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    building = delete_building_crud(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"detail": "Building deleted successfully"}
