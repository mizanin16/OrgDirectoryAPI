from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.crud.building import (
    create_building,
    update_building,
    delete_building,
    get_all_buildings,
    get_building
)
from app.core.dependencies import get_db

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=list[BuildingResponse])
def get_buildings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_buildings(db, skip, limit)


@router.get("/{building_id}", response_model=BuildingResponse)
def get_building(building_id: int, db: Session = Depends(get_db)):
    building = get_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.post("/", response_model=BuildingResponse)
def create_building(building_data: BuildingCreate, db: Session = Depends(get_db)):
    return create_building(db, building_data)


@router.put("/{building_id}", response_model=BuildingResponse)
def update_building(building_id: int, building_data: BuildingUpdate, db: Session = Depends(get_db)):
    building = update_building(db, building_id, building_data)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.delete("/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    building = delete_building(db, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"detail": "Building deleted successfully"}
