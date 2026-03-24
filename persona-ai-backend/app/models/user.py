from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Data the user sends when registering."""
    email: EmailStr        # validates email format automatically
    password: str          # plain text — will be hashed before storing

class UserResponse(BaseModel):
    """
    What the API returns — NEVER includes hashed_password.
    Safe to send back to the client.
    """
    user_id: str
    email: str
    created_at: str
    is_active: bool

class UserInDB(UserResponse):
    """
    Internal model used only inside the backend.
    Adds hashed_password — never returned in API responses.
    """
    hashed_password: str