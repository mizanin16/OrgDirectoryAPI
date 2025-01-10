from pydantic import BaseModel, Field
from typing import List

class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    phone_numbers: List[str] = Field(..., example=["+123456789"])
    building_id: int | None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: int

    class Config:
        from_attributes = True
