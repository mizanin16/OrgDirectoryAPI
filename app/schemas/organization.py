from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class OrganizationBase(BaseModel):
    name: str = Field(..., max_length=255)
    phone_numbers: List[str] = Field(..., json_schema_extra={"example": ["+123456789"]})
    building_id: int | None


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None
    phone_numbers: Optional[List[str]] = None
    building_id: Optional[int] = None
