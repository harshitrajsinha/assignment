from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(min_length=1, max_length=10_000, description="The user's message")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context for the LLM")
    session_id: Optional[str] = Field(default=None, description="Session identifier for tracking")

# Receive question from user not message
# Do not receive context from user
# generate random session id and maintain session for the user (need to figure out)


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(description="The LLM's response")
    model_used: str = Field(description="The model that was used")
    tokens_used: Optional[int] = Field(default=None, description="Number of tokens used")
    latency_ms: Optional[int] = Field(default=None, description="Request latency in milliseconds")

# do not return model used, tokens used, latency ms to user