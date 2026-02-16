from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignupRequest(BaseModel):
    """Schema for user signup request"""
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Schema for user login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user response (no password)"""
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Schema for auth response with JWT token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
