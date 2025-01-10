from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.models.building import Building
from app.schemas.organization import OrganizationCreate


def get_organization_crud(db: Session, org_id: int):
    return db.query(Organization).filter(Organization.id == org_id).first()


def get_organizations_crud(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Organization).offset(skip).limit(limit).all()


def create_organization_crud(db: Session, org: OrganizationCreate):
    # Проверяем существование здания
    building = db.query(Building).filter(Building.id == org.building_id).first()
    if not building:
        raise ValueError(f"Building with id {org.building_id} does not exist")

    new_org = Organization(**org.model_dump())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org


def update_organization_crud(db: Session, org_id: int, org_data: OrganizationCreate):
    org = get_organization_crud(db, org_id)
    if not org:
        return None

    # Проверяем существование здания
    building = db.query(Building).filter(Building.id == org_data.building_id).first()
    if not building:
        raise ValueError(f"Building with id {org_data.building_id} does not exist")

    for key, value in org_data.model_dump().items():
        setattr(org, key, value)
    db.commit()
    db.refresh(org)
    return org


def delete_organization_crud(db: Session, org_id: int):
    org = get_organization_crud(db, org_id)
    if not org:
        return None
    db.delete(org)
    db.commit()
    return org
