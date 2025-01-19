from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class ActivityResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    children: List['ActivityResponse'] = []
    organizations: List[int] = []
    organizations_count: int = 0
    model_config = ConfigDict(from_attributes=True)