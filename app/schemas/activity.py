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


class ActivityResponse(ActivityBase):
    id: int
    children: Optional[List[int]] = []
    organizations: Optional[List[int]] = []
    organizations_count: int = 0

    model_config = ConfigDict(from_attributes=True)


    def __init__(self, **data):
        super().__init__(**data)
        self.organizations_count = len(data.get("organizations", []))
        if not self.children:
            self.children = None
        if not self.organizations:
            self.organizations = None