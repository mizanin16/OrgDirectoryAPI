from pydantic import BaseModel, ConfigDict
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
    organizations_count: int = 0

    model_config = ConfigDict(from_attributes=True)


    def __init__(self, **data):
        super().__init__(**data)
        self.organizations_count = len(data.get("organizations", []))
