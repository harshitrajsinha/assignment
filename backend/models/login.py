from pydantic import BaseModel, EmailStr, Field, field_validator

# User is expected to pass request in this form
class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str

    # password must be between 8-12 chars, have one atleast one digit and one special char
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not 8 <= len(value) <= 12:
            raise ValueError("Password must be between 8-12 chars")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        if not any(not char.isalnum() for char in value):
            raise ValueError("Password must contain at least one special character")

        return value


# Response will be received back to user in this form
class LoginResponse(BaseModel):
    authenticated: bool