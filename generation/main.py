import uvicorn
import os
from time import perf_counter
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Response

from routes import health, generate
from middleware.metrics import latency_store

load_dotenv()

IS_PROD = os.getenv("ENVIRONMENT") == "production"


app = FastAPI(
    title="LLM Gateway",
    description="Gateway service for LLM providers with OpenAI integration",
    docs_url=None if IS_PROD else "/docs",
    redoc_url=None if IS_PROD else "/redoc",
    openapi_url=None if IS_PROD else "/openapi.json",
)


@app.middleware("http")
async def capture_latency(request: Request, call_next) -> Response:
    """
    Middleware to capture request latency.
    """
    started_at = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        latency_store.record(request.url.path, started_at, 500)
        raise

    latency_store.record(request.url.path, started_at, response.status_code)
    return response


# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(generate.router, prefix="/api/v1", tags=["generate"])


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=not IS_PROD, workers=2 if IS_PROD else 1)