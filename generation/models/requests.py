from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class GenerateRequest(BaseModel):
    """Request model for LLM generation endpoint."""
    question: str = Field(min_length=1, max_length=10_000)
    # session_id: Optional[str]  = Field(default=None)


class GenerateResponse(BaseModel):
    """Response model for LLM generation endpoint."""
    answer: str 
    model_used: str 
    tokens_used: Optional[int] = Field(default=0)
    latency_ms: Optional[int] = Field(default=0)