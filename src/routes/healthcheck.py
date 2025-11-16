from typing import Any, Dict

from fastapi import APIRouter

router = APIRouter(prefix="/healthcheck")


@router.get("")
def healthcheck() -> Dict[str, Any]:
    """Healthcheck endpoint to verify the service is running."""
    return {"status": "ok"}
