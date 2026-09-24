from pydantic import BaseModel
from typing import TypedDict

class RouteStats(TypedDict):
    requests: (int | float) = 0
    errors: (int | float) = 0
    average_latency_ms: (int | float) = 0

class MetricsResponse(BaseModel):
    routes: dict[str, RouteStats]