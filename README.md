## Summary

QnA API is a versioned FastAPI service with a SQLModel PostgreSQL user store,
bcrypt login validation, and simple in-memory latency tracking.

## API routes

All endpoints are prefixed with `/api/v1` and are defined with FastAPI
`APIRouter` instances. Each route lives in its own module under `routes/`.

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/health` | Returns the service health status. |
| `GET` | `/api/v1/metrics` | Returns request count, error count, and average latency for tracked endpoints. |
| `POST` | `/api/v1/chat` | Returns a static dummy chat response for now. |
| `POST` | `/api/v1/auth/login` | Validates an email and password against a user in PostgreSQL. |

`/metrics` captures latency for `/chat` and `/auth/login` with an in-memory
total request count, error count, and cumulative request duration. Average
latency is calculated from the cumulative duration divided by request count.
The data resets when the application restarts.

## Project structure

```text
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

## Seed users

`scripts.seed_users` creates missing users and makes existing seed users active
with their configured roles. It does not overwrite an existing user's password.
Set a development-only password first, then run the module from the repository
root:

```bash
export SEED_USER_PASSWORD="choose-a-strong-development-password"
python -m scripts.seed_users
```

| Email | Role |
| --- | --- |
| `admin@eliciusenergy.com` | `admin` |
| `harshit@gmail.com` | `admin` |
| `newuser@gmail.com` | `user` |
