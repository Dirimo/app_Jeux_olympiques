from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

#Model utilisateur

class UserRole(str, Enum):
    CLIENT = "client"
    ADMIN= "admin"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    nom : str
    prenom : str
    is_active: bool = True
    role: UserRole = UserRole.CLIENT

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    clef_compte: str # Clé secrète générée pour à l'inscription