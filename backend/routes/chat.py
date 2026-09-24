import os
import httpx
from fastapi import APIRouter, HTTPException, status

from models.chat import ChatRequest, ChatResponse

router = APIRouter()

# Gateway configuration
GATEWAY_URL = os.getenv("LLM_GATEWAY_URL")
GATEWAY_TIMEOUT = int(os.getenv("LLM_GATEWAY_TIMEOUT"))


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint that forwards requests to the LLM gateway.
    """
    try:
        # Prepare request payload for gateway
        gateway_request = {
            "question": request.message
            # "context": request.context,
            # "session_id": request.session_id
        }
        
        # Call LLM gateway
        async with httpx.AsyncClient(timeout=GATEWAY_TIMEOUT) as client:
            response = await client.post(
                f"{GATEWAY_URL}/api/v1/generate",
                json=gateway_request
            )
            response.raise_for_status()
            
            # Parse gateway response
            gateway_data = response.json()
            
            # Map gateway response to our response model
            return ChatResponse(
                response=gateway_data["answer"],
                model_used=gateway_data["model_used"],
                tokens_used=gateway_data.get("tokens_used"),
                latency_ms=gateway_data.get("latency_ms")
            )
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="LLM gateway request timed out"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"LLM gateway error: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Failed to connect to LLM gateway: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )
