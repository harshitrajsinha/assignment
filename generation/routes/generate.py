from fastapi import APIRouter, HTTPException, status

from models.requests import GenerateRequest, GenerateResponse
from services.providers import register
import logging
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
import json

load_dotenv()
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """
    Generate a response using the configured LLM provider.
    """
    try:
        # Create provider instance
        LLM_PROVIDER=os.getenv("LLM_PROVIDER")
        provider = register.ProviderFactory.create_provider(LLM_PROVIDER)
        
        # Generate response
        result = await provider.generate(
            prompt=request.question
            # session_id=request.session_id
        )
        
        return GenerateResponse(**result)
        
    except ValueError as e:
        logger.error(
            "LLM provider configuration error: provider=%s and error=%s",
            LLM_PROVIDER, str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    
    except RuntimeError as e:
        # Provider errors
        # print(f"LLM provider error: {str(e)}")
        logger.error(
            "LLM provider failed: provider=%s, error =%s",
            LLM_PROVIDER, str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM provider error: {str(e)}"
        )
    
    except Exception as e:
        logger.error(
            "Unexpected error during LLM generation: provider=%s, error =%s",
            LLM_PROVIDER, str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


#########  WORK IN PROGRESS ########


@router.post("/generate/stream")
async def generate(request: GenerateRequest):
    """
    Generate a streamed response using the configured LLM provider.
    """
    try:
        # Create provider instance
        LLM_PROVIDER=os.getenv("LLM_PROVIDER")
        provider = register.ProviderFactory.create_provider(LLM_PROVIDER)

        
        async for chunk in provider.generate_stream(
            prompt=request.question,
            context=request.context,
            session_id=request.session_id
        ):  
            print(json.dumps(chunk) + "\n")
            # yield json.dumps(chunk) + "\n"

        
    except ValueError as e:
        # Configuration errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {str(e)}"
        )
    except RuntimeError as e:
        # Provider errors
        # print(f"LLM provider error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM provider error: {str(e)}"
        )
    except Exception as e:
            # Unexpected errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )