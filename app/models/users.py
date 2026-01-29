from pydantic import BaseModel, EmailStr, field_validator
from typing import Literal, Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class Register(UserBase):
    username: str
    role: Literal["admin", "member"] = "member"
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None

class Login(UserBase):
    pass

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: Literal["admin", "member"]
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    created_at: datetime
