from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

class HealthResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Returns a static response for health check
    """
    return HealthResponse(status="ok")
