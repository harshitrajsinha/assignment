# LLM Gateway Microservice

A FastAPI-based microservice that provides a unified interface for LLM providers, starting with OpenAI integration. The service uses environment-based configuration and is designed to be easily extended with additional providers.

## Architecture Overview

```
Client → QnA Backend (/chat) → LLM Gateway → OpenAI API
                              ↓
                        Health Endpoint
                        Generate Endpoint  
                        Metrics Middleware
```

## Features

- **Provider Abstraction**: Clean interface for easy addition of new LLM providers
- **Environment Configuration**: All settings managed via environment variables
- **Health Monitoring**: Built-in health check endpoint
- **Metrics Tracking**: Request latency and error tracking
- **Error Handling**: Graceful degradation when providers fail
- **Extensible Design**: Easy to add new providers (Gemini, Claude, etc.)

## API Endpoints

### Health Check
```
GET /api/v1/health
Response: { "status": "ok", "provider": "openai", "model": "gpt-4" }
```

### Generate Response
```
POST /api/v1/generate
Request: { "question": str, "context": Optional[dict], "session_id": Optional[str] }
Response: { "answer": str, "model_used": str, "tokens_used": Optional[int], "latency_ms": Optional[int] }
```

## Configuration

Configuration is managed through environment variables:

```env
LLM_PROVIDER=openai              # LLM provider (currently only openai supported)
LLM_MODEL=gpt-4                  # Model name to use
OPENAI_API_KEY=sk-...            # OpenAI API key
LLM_TEMPERATURE=0.7              # Generation temperature (0.0-1.0)
LLM_MAX_TOKENS=1000              # Maximum tokens in response
LLM_TIMEOUT=30                    # Request timeout in seconds
ENVIRONMENT=development          # Environment (development/production)
```

## Project Structure

```
generation/
├── main.py                 # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Container configuration
├── README.md              # This file
├── models/
│   ├── __init__.py
│   ├── config.py          # LLM configuration models
│   └── requests.py        # API request/response models
├── routes/
│   ├── __init__.py
│   ├── generate.py        # Main generation endpoint
│   └── health.py          # Health check
├── services/
│   ├── __init__.py
│   ├── config.py          # Environment-based configuration management
│   └── providers/
│       ├── __init__.py
│       ├── base.py        # Abstract provider interface
│       ├── openai.py      # OpenAI implementation
│       └── factory.py     # Provider factory
└── middleware/
    ├── __init__.py
    └── metrics.py         # Request tracking and latency
```

## Implementation Status

- [x] Project structure setup
- [x] Environment-based configuration management
- [x] Provider abstraction layer (BaseProvider, factory)
- [x] OpenAI provider implementation
- [x] FastAPI application with health and generate routes
- [x] Metrics middleware for request tracking
- [x] Basic error handling
- [x] Backend chat route integration
- [x] Docker setup and docker-compose integration
- [x] Basic testing script
- [x] Complete documentation

## Setup Instructions

### Local Development

1. **Install dependencies:**
```bash
cd generation
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. **Run the service:**
```bash
python main.py
```

The service will start on `http://localhost:8001`

### Docker Setup

1. **Build the image:**
```bash
docker build -t llm-gateway:latest .
```

2. **Run the container:**
```bash
docker run -p 8001:8001 \
  -e OPENAI_API_KEY=your-api-key \
  -e LLM_MODEL=gpt-4 \
  llm-gateway:latest
```

## Adding New Providers

The architecture is designed to make adding new providers straightforward:

1. **Create provider class** in `services/providers/` (e.g., `gemini.py`)
2. **Implement the BaseProvider interface:**
   - `generate(prompt, **kwargs)` method
   - `_validate_config()` method
   - `get_model_info()` method
3. **Register provider** in `services/providers/factory.py`
4. **Add dependencies** to `requirements.txt`
5. **Add environment variables** for API keys
6. **Update configuration** in `services/config.py`

Example for adding Gemini:

```python
# services/providers/gemini.py
from .base import BaseProvider

class GeminiProvider(BaseProvider):
    def _validate_config(self):
        if not self.config.api_key:
            raise ValueError("Gemini API key is required")
    
    def generate(self, prompt: str, **kwargs):
        # Implementation using Google Gemini API
        pass
    
    def get_model_info(self):
        return {"provider": "gemini", "model": self.config.model}
```

```python
# services/providers/factory.py
from .gemini import GeminiProvider

ProviderFactory.register_provider("gemini", GeminiProvider)
```

## Usage Example

### Direct API Call

```bash
curl -X POST http://localhost:8001/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the capital of France?",
    "context": {"user": "test-user"},
    "session_id": "session-123"
  }'
```

### Response

```json
{
  "answer": "The capital of France is Paris.",
  "model_used": "gpt-4",
  "tokens_used": 25,
  "latency_ms": 1234
}
```

## Integration with QnA Backend

The backend chat route will be updated to call this gateway:

```python
# backend/routes/chat.py
import httpx

@router.post("/chat")
async def chat(request: ChatRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://llm-gateway:8001/api/v1/generate",
            json={"question": request.message},
            timeout=30.0
        )
        return response.json()
```

## Key Design Decisions

- **OpenAI-First**: Start with OpenAI only, but architecture supports easy addition of providers
- **Environment Config**: Configuration via environment variables only (no runtime updates)
- **Provider Abstraction**: Clean interface allows easy addition of new providers later
- **FastAPI**: Consistent with existing backend stack
- **Separate Service**: Enables independent scaling and deployment
- **Hidden Service**: Only health and generate endpoints exposed
- **Metrics Middleware**: Request tracking and latency monitoring
- **Error Handling**: Graceful degradation when OpenAI fails

## Security Considerations

- **API Key Management**: Use environment variables or secret management systems
- **Rate Limiting**: Implement rate limiting for production use
- **Input Validation**: All inputs are validated using Pydantic models
- **Error Messages**: Avoid exposing sensitive information in error responses

## Monitoring and Observability

- **Health Endpoint**: `/api/v1/health` for service health checks
- **Metrics Middleware**: Tracks request count, errors, and latency
- **Structured Logging**: Implement structured logging for production
- **Error Tracking**: Add error tracking (Sentry, etc.) for production

## Future Enhancements

- [ ] Add support for streaming responses
- [ ] Implement request caching
- [ ] Add rate limiting and quota management
- [ ] Implement cost tracking and estimation
- [ ] Add support for more providers (Gemini, Claude, local models)
- [ ] Implement request/response logging
- [ ] Add A/B testing capabilities for different models
- [ ] Implement retry logic with exponential backoff

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your OpenAI API key is valid and has sufficient credits
2. **Timeout Errors**: Increase `LLM_TIMEOUT` if requests are taking too long
3. **Model Not Found**: Verify the model name is correct and available in your OpenAI account
4. **Import Errors**: Ensure all dependencies are installed correctly

### Debug Mode

Set `ENVIRONMENT=development` to enable:
- API documentation at `/docs`
- Detailed error messages
- Auto-reload on file changes

## License

This microservice is part of the QnA API project.