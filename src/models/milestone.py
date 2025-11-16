from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from src.models.base_model import BaseTable


class Milestone(BaseTable, table=True):
    """DB model for a project milestone."""

    # foreign key to projects table (uses Project.id primary key)
    project_id: int | None = Field(default=None, foreign_key="project.id", index=True)

    name: str
    description: Optional[str] = None
    amount: float


class MilestoneCreate(BaseModel):
    """Schema for creating a new milestone (excludes id and timestamps)."""
    project_id: int
    name: str
    description: Optional[str] = None
    amount: float


class MilestoneUpdate(BaseModel):
    """Schema for updating a milestone (all fields optional)."""
    project_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None





