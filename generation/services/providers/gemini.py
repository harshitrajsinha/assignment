from typing import Dict, Any, Optional
import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_MODEL = os.getenv("LLM_MODEL")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7")),
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "500")),

class GeminiProvider():
    """Gemini provider implementation."""
    
    def __init__(self):
        self.client = genai.Client()
    
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:

        start_time = time.time()
        
        try:

            context = kwargs.get("context")
            
            # Calling OpenAI API
            response = self.client.interactions.create(
                model= GEMINI_MODEL,
                system_instruction="",
                input= [{"type": "text", "text": prompt}],
                generation_config={
                    "temperature": 0.7
                }
            )
            
            # Extract response data
            # print(response)
            answer = response.output_text
            model_used = response.model
            tokens_used = response.usage.total_tokens
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "answer": answer,
                "model_used": model_used,
                "tokens_used": tokens_used,
                "latency_ms": latency_ms
            }
            
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {str(e)}") from e


    def generate_stream(self, prompt: str, **kwargs):

        start_time = time.time()
                
        try:

            context = kwargs.get("context")
            
            # Calling OpenAI API
            response = self.client.interactions.create(
                model= GEMINI_MODEL,
                system_instruction="",
                input= [{"type": "text", "text": prompt}],
                generation_config={
                    "temperature": 0.7
                },
                stream = True
            )
            
            for event in response:

                # print("EVENT TYPE:", event.event_type)
                # print("EVENT:", event)

                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                # continue

                # Stream actual model output
                if (
                    event.event_type == "step.delta"
                    and getattr(event.delta, "type", None) == "text"
                ):
                    yield {
                        "type": "text",
                        "text": event.delta.text,
                    }

                # Capture final metadata
                elif event.event_type == "interaction.completed":
                    model_used = event.interaction.model
                    tokens_used = event.interaction.usage.total_tokens

                    latency_ms = int((time.time() - start_time) * 1000)

                    # Send metadata as the final chunk
                    yield {
                        "type": "metadata",
                        "model_used": model_used,
                        "tokens_used": tokens_used,
                        "latency_ms": latency_ms,
                    }
            
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {str(e)}") from e