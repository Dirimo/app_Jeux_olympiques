# backend/schemas/user_schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    nom: str
    prenom: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    nom: str
    prenom: str
    role: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True

