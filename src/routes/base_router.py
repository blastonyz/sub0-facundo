from fastapi import APIRouter

from src.routes.healthcheck import router as healthcheck_router
from src.routes.v1.arkiv import router as arkiv_router

base_router = APIRouter()

base_router.include_router(healthcheck_router)
base_router.include_router(arkiv_router, prefix="/api/v1", tags=["projects"])
