import uvicorn
from contextlib import asynccontextmanager
from time import perf_counter
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Request, Response

from routes import auth, chat, health, metrics
from services.database import close_db, create_tables
from services.metrics import latency_store

load_dotenv()

IS_PROD=os.getenv("ENVIRONMENT") == "production"


@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield
    close_db()


app = FastAPI(
    title="QnA API",
    description="QnA API",
    docs_url=None if IS_PROD else "/docs",
    redoc_url=None if IS_PROD else "/redoc",
    openapi_url=None if IS_PROD else "/openapi.json",
    lifespan=lifespan
)

# Middleware to capture latency. Start time before processing and then record before sending response
@app.middleware("http")
async def capture_latency(request: Request, call_next) -> Response:
    started_at = perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        latency_store.record(request.url.path, started_at, 500)
        raise

    latency_store.record(request.url.path, started_at, response.status_code)
    return response


app.include_router(health.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)