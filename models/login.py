from pydantic import BaseModel, EmailStr, Field

# User is expected to pass request in this form
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=72)

# Response will be received back to user in this form
class LoginResponse(BaseModel):
    authenticated: bool