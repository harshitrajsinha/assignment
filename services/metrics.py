from threading import Lock
from time import perf_counter

TRACKED_PATHS = ("/api/v1/chat", "/api/v1/auth/login")

# using lock to avoid race condition
class LatencyStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._routes = {
            path: {"requests": 0, "errors": 0, "total_latency_ms": 0.0}
            for path in TRACKED_PATHS
        }
    
    def record(self, path: str, started_at: float, status_code: int) -> None:
        if path not in self._routes:
            return

        elapsed_ms = (perf_counter() - started_at) * 1_000
        with self._lock:
            metrics = self._routes[path]
            metrics["requests"] += 1
            metrics["total_latency_ms"] += elapsed_ms
            if status_code >= 400:
                metrics["errors"] += 1

    # Returns the recorded metrics
    def snapshot(self) -> dict[str, dict[str, int | float]]:
        with self._lock:
            return {
                path: {
                    "requests": values["requests"],
                    "errors": values["errors"],
                    "average_latency_ms": round(
                        values["total_latency_ms"] / values["requests"], 2
                    )
                    if values["requests"]
                    else 0.0,
                }
                for path, values in self._routes.items()
            }


latency_store = LatencyStore()
