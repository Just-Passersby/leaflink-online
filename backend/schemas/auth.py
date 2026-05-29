from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50, examples=["just-passersby"])
    email: EmailStr = Field(..., examples=["user@example.com"])
    password: str = Field(..., min_length=8, examples=["securepassword123"])


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["just-passersby"])
    password: str = Field(..., examples=["securepassword123"])


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
