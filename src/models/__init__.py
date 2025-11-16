"""
Models module.

This file imports all SQLModel models to ensure SQLAlchemy can properly
resolve relationships and foreign keys at application startup.

Import order matters: base first, then dependencies (no circular deps at import time),
then derived models.
"""

# Import base first
from src.models.base_model import BaseTable

# Import models in dependency order
# NOTE: Relationships use sa_relationship_kwargs to avoid circular imports
from src.models.project import Project, ProjectCreate, ProjectUpdate
from src.models.milestone import Milestone, MilestoneCreate, MilestoneUpdate
from src.models.sponsor import (
    SponsoredProject,
    SponsoredProjectCreate,
    SponsoredProjectUpdate,
    SponsorRequest,
    SponsoredProjectOut,
)
from src.models.evaluate import EvaluateResponse

# Relations configuration (if needed in future)
# from src.models.relations import *

__all__ = [
    "BaseTable",
    "Project",
    "ProjectCreate",
    "ProjectUpdate",
    "Milestone",
    "MilestoneCreate",
    "MilestoneUpdate",
    "SponsoredProject",
    "SponsoredProjectCreate",
    "SponsoredProjectUpdate",
    "SponsorRequest",
    "SponsoredProjectOut",
    "EvaluateResponse",
]

