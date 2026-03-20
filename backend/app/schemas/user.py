"""
Pydantic schemas for user responses
"""
from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
