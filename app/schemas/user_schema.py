from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str


