from fastapi import APIRouter
from models.metrics import MetricsResponse

from services.metrics import latency_store

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
async def metrics() -> MetricsResponse:
    """
    Returns the recorded metrics
    """
    return MetricsResponse(routes=latency_store.snapshot())
