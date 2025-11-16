from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from src.models.base_model import BaseTable


class Project(BaseTable, table=True):
    """DB model for a project."""

    project_id: str = Field(index=True, nullable=False)
    name: str
    repo: str
    description: Optional[str] = None
    budget: float









class ProjectCreate(BaseModel):
    """Schema for creating a new project (excludes read-only fields)."""
    
    project_id: str
    name: str
    repo: str
    description: Optional[str] = None
    budget: float


class ProjectUpdate(BaseModel):
    """Schema for updating a project (all fields optional)."""
    
    project_id: Optional[str] = None
    name: Optional[str] = None
    repo: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[float] = None
