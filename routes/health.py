from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """
    Returns a static response for health check
    """
    return {"status": "ok"}
