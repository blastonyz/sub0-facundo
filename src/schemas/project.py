from typing import List, Optional

from pydantic import BaseModel, Field

from src.schemas.milestone import MilestoneRead


class ProjectBase(BaseModel):
    project_id: str
    name: str
    repo: str
    description: Optional[str] = None
    budget: float
    milestones: List[MilestoneRead] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass