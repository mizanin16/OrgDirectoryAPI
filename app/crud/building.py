from sqlalchemy.orm import Session
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate


def get_building(db: Session, building_id: int):
    return db.query(Building).filter(Building.id == building_id).first()


def get_all_buildings(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Building).offset(skip).limit(limit).all()


def create_building(db: Session, building_data: BuildingCreate):
    building = Building(**building_data.dict())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


def update_building(db: Session, building_id: int, building_data: BuildingUpdate):
    building = get_building(db, building_id)
    if not building:
        return None
    for key, value in building_data.dict(exclude_unset=True).items():
        setattr(building, key, value)
    db.commit()
    db.refresh(building)
    return building


def delete_building(db: Session, building_id: int):
    building = get_building(db, building_id)
    if building:
        db.delete(building)
        db.commit()
    return building
