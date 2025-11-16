from fastapi import FastAPI

# Import models to ensure SQLAlchemy can resolve relationships
from src.models import (
    BaseTable,
    Project,
    Milestone,
    SponsoredProject,
    EvaluateResponse,
)
from src.routes.base_router import base_router

app = FastAPI(title="Sub0 Funding Oracle API")

app.include_router(base_router)
