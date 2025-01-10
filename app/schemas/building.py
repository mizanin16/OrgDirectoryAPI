from pydantic import BaseModel
from typing import Optional, List


class BuildingBase(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class BuildingResponse(BuildingBase):
    id: int
    organizations: Optional[List[int]] = []

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.organizations:
            self.organizations = None