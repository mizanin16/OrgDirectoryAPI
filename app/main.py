from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
from app.core.db import SessionLocal, engine, Base
from app.models import Organization  # предполагаем, что модель уже есть

# Инициализация приложения и базы
app = FastAPI()
Base.metadata.create_all(bind=engine)

# Зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic-схема для валидации данных
class OrganizationCreate(BaseModel):
    name: str = Field(..., max_length=255)
    phone_numbers: List[str] = Field(..., example=["+123456789"])
    building_id: int

class OrganizationResponse(OrganizationCreate):
    id: int

    class Config:
        orm_mode = True

# CRUD эндпоинты
@app.post("/organizations/", response_model=OrganizationResponse)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    new_org = Organization(**org.dict())
    db.add(new_org)
    db.commit()
    db.refresh(new_org)
    return new_org

@app.get("/organizations/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@app.put("/organizations/{org_id}", response_model=OrganizationResponse)
def update_organization(org_id: int, org_data: OrganizationCreate, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    for key, value in org_data.dict().items():
        setattr(org, key, value)
    db.commit()
    db.refresh(org)
    return org

@app.delete("/organizations/{org_id}")
def delete_organization(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(org)
    db.commit()
    return {"message": "Organization deleted successfully"}
