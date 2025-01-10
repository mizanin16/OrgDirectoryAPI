from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.organization import (
    get_organization, get_organizations,
    create_organization, update_organization, delete_organization
)
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.core.dependencies import get_db

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("/", response_model=OrganizationResponse)
def create_new_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    try:
        return create_organization(db, org)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{org_id}", response_model=OrganizationResponse)
def update_existing_organization(org_id: int, org_data: OrganizationCreate, db: Session = Depends(get_db)):
    try:
        updated_org = update_organization(db, org_id, org_data)
        if not updated_org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return updated_org
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{org_id}")
def delete_existing_organization(org_id: int, db: Session = Depends(get_db)):
    deleted_org = delete_organization(db, org_id)
    if not deleted_org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {"message": "Organization deleted successfully"}


@router.get("/", response_model=list[OrganizationResponse])
def read_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_organizations(db, skip=skip, limit=limit)


@router.get("/{org_id}", response_model=OrganizationResponse)
def read_organization(org_id: int, db: Session = Depends(get_db)):
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
