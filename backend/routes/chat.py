import os
import logging

import httpx
from fastapi import APIRouter, HTTPException, status
from dotenv import load_dotenv

from models.chat import ChatRequest, ChatResponse

load_dotenv()
logger = logging.getLogger(__name__)

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
            "question": request.question
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

            logger.info(
                "LLM gateway response received with status code: status_code=%s",
                response.status_code,
            )
            
            # Map gateway response to our response model
            return ChatResponse(
                response=gateway_data["answer"],
                tokens_used=gateway_data.get("tokens_used"),
            )
            
    except httpx.TimeoutException:
        logger.warning(
            "LLM gateway request timed out: timeout=%ss",
            GATEWAY_TIMEOUT,
        )
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="We are experiencing high requests. Try again after sometime"
        )
    
    except httpx.HTTPStatusError as e:
        logger.error(
            "LLM gateway returned error: status_code=%s and error=%s",
            e.response.status_code, e.response.text
        )
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Could not resolve request right now, try again after some time"
        )
    
    except httpx.RequestError as e:
        logger.error(
            "Failed to connect to LLM gateway: error=%s",
            str(e),
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not resolve request right now, try again after some time"
        )
    
    except Exception as e:
        logger.exception("Unexpected error while processing chat request: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error. Please contact support team"
        )
