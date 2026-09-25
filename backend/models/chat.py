from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    question: str = Field(min_length=1, max_length=10_000, description="The user's message")

# generate random session id and maintain session for the user (need to figure out)


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str
    tokens_used: Optional[int] = Field(default=None)
