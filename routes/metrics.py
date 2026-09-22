from fastapi import APIRouter

from services.metrics import latency_store

router = APIRouter()


@router.get("/metrics")
async def metrics() -> dict[str, dict[str, dict[str, int | float]]]:
    return {"routes": latency_store.snapshot()}
