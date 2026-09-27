from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str = Field(min_length=1, max_length=10_000, example="What is today's date and time?")

# generate random session id and maintain session for the user (need to figure out)


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    tokens_used: Optional[int] = Field(default=None)
