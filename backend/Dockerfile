FROM python:3.12-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy application code
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

# Will perform health check via docker compose

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]