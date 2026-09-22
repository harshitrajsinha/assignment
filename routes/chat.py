from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

# move this to models
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)


@router.post("/chat")
async def chat(_: ChatRequest) -> dict[str, str]:
    """
    Dummy route as of now
    """
    return {"response": "This is a static chat response."}
