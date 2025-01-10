from sqlalchemy.orm import Session
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


def get_organization(db: Session, org_id: int) -> Organization:
    return db.query(Organization).filter(Organization.id == org_id).first()


def get_organizations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Organization).offset(skip).limit(limit).all()


def create_organization(db: Session, org_data: OrganizationCreate) -> Organization:
    new_org = Organization(**org_data.dict())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org


def update_organization(db: Session, org_id: int, org_data: OrganizationUpdate) -> Organization:
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        return None
    for key, value in org_data.dict(exclude_unset=True).items():
        setattr(org, key, value)
    db.commit()
    db.refresh(org)
    return org


def delete_organization(db: Session, org_id: int) -> bool:
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        return False
    db.delete(org)
    db.commit()
    return True
