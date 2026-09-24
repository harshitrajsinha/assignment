from typing import Dict, Any
import time
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAPI_MODEL = os.getenv("LLM_MODEL")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7")),
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500")),


# class OpenAIProvider(BaseProvider):
class OpenAIProvider():
    """OpenAI provider implementation."""
    
    def __init__(self):
        self.client = OpenAI(timeout=float(30), max_retries=3)  # API key will be read directly from environment variable (as per OpenAI recommended docs))
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:

        start_time = time.time()
        
        try:
            context = kwargs.get("context")
            
            # Calling OpenAI API
            response = self.client.chat.completions.create(
                model= OPENAPI_MODEL,
                messages= [{"role": "user", "content": prompt}, {"role": "system", "content": f"Context: {context}"}],
                temperature= LLM_TEMPERATURE,
                max_tokens= LLM_MAX_TOKENS
            )
            
            # Extract response data
            answer = response.choices[0].message.content
            model_used = response.model
            tokens_used = response.usage.total_tokens if response.usage else None
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "answer": answer,
                "model_used": model_used,
                "tokens_used": tokens_used,
                "latency_ms": latency_ms
            }
            
        except Exception as e:
            raise RuntimeError(f"OpenAI generation failed: {str(e)}") from e