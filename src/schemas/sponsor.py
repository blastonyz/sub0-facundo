
from typing import Optional

from pydantic import BaseModel

from src.schemas.project import ProjectRead


class SponsorRequest(BaseModel):
    project: ProjectRead
    ai_score: float
    decision: str
    contract_address: str

class SponsoredProjectOut(BaseModel):
    project_id: str
    name: str
    repo: str
    ai_score: float
    status: str
    contract_address: str
    chain: str
    budget: float
    description: Optional[str] = None
    _entity_key: Optional[str] = None