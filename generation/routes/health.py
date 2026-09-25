from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    provider: str
    model: str


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """
    Returns a static response for health check
    """
    return HealthResponse(
        status="ok",
        provider=os.getenv("LLM_PROVIDER"),
        model=os.getenv("LLM_MODEL"),
    )
