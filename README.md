## Summary

QnA API is a versioned FastAPI service with a SQLModel PostgreSQL user store,
bcrypt login validation, and LLM integration through a dedicated gateway service.
The system consists of two main services: the QnA backend and an LLM gateway.

## API routes

All endpoints are prefixed with `/api/v1` and are defined with FastAPI
`APIRouter` instances. Each route lives in its own module under `routes/`.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Returns the service health status. |
| `GET` | `/api/v1/metrics` | Returns request count, error count, and average latency for tracked endpoints. |
| `POST` | `/api/v1/chat` | Forwards chat requests to the LLM gateway and returns AI-generated responses. |
| `POST` | `/api/v1/auth/login` | Validates an email and password against a user in PostgreSQL. |

`/metrics` captures latency for `/chat` and `/auth/login` with an in-memory
total request count, error count, and cumulative request duration. Average
latency is calculated from the cumulative duration divided by request count.
The data resets when the application restarts.

## Project structure

```text
backend/
  models/
    chat.py
    login.py
  routes/
    auth.py
    chat.py
    health.py
    metrics.py
  scripts/
    seed_users.py
  services/
    database.py
    metrics.py

generation/
  models/
    config.py
    requests.py
  routes/
    generate.py
    health.py
  services/
    config.py
    providers/
      base.py
      openai.py
      factory.py
  middleware/
    metrics.py
```

## Database design

The PostgreSQL `users` table is defined by the SQLModel `User` class.

| Column | Type | Constraints / default |
| --- | --- | --- |
| `id` | UUID | Primary key; application-generated with `uuid4`. |
| `email` | TEXT | Required; indexed; maximum 320 characters. |
| `password_hash` | TEXT | Required; stores a bcrypt password hash. |
| `is_active` | BOOLEAN | Required; defaults to `true`. |
| `role` | `UserRole` enum | Required; `admin` or `user`; defaults to `user`. |
| `created_at` | TIMESTAMPTZ | UTC timestamp assigned when the model is created. |
| `updated_at` | TIMESTAMPTZ | UTC timestamp assigned when the model is created. |

Passwords are never stored as raw text and cannot be unhashed. On login, the
server retrieves the stored bcrypt hash and uses bcrypt's verification function
to compare it safely with the submitted password.

## LLM Gateway

The LLM Gateway is a separate FastAPI microservice that provides a unified interface
for AI model providers. Currently, it supports OpenAI with the following features:

- **Provider Abstraction**: Clean interface for easy addition of new LLM providers
- **Environment Configuration**: All settings managed via environment variables
- **Health Monitoring**: Built-in health check endpoint
- **Metrics Tracking**: Request latency and error tracking
- **Error Handling**: Graceful degradation when providers fail

### Gateway Architecture

```
Client → QnA Backend (/chat) → LLM Gateway → OpenAI API
                              ↓
                        Health Endpoint
                        Generate Endpoint  
                        Metrics Middleware
```

### Gateway Configuration

The gateway is configured through environment variables:

```env
LLM_PROVIDER=openai              # LLM provider (currently only openai supported)
LLM_MODEL=gpt-4                  # Model name to use
OPENAI_API_KEY=sk-...            # OpenAI API key
LLM_TEMPERATURE=0.7              # Generation temperature (0.0-1.0)
LLM_MAX_TOKENS=1000              # Maximum tokens in response
LLM_TIMEOUT=30                    # Request timeout in seconds
```

For detailed information about the LLM gateway, see the [generation/README.md](generation/README.md).

## Seed users

`scripts.seed_users` creates dummy users and makes existing seed users active
with their configured roles.

| Email | Role |
| --- | --- |
| `admin@eliciusenergy.com` | `admin` |
| `harshit@gmail.com` | `admin` |
| `newuser@gmail.com` | `user` |


<hr>

### Run application via docker compose

```docker compose --build --env-file .env up```