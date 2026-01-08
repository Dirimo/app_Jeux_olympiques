# app/models/user.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum

if TYPE_CHECKING:
    from .ticket import Ticket

# Model utilisateur

class UserRole(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    nom: str
    prenom: str
    is_active: bool = True
    role: UserRole = UserRole.CLIENT

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    clef_compte: str  # Clé secrète générée à l'inscription
    
    # Relations
    tickets: List["Ticket"] = Relationship(back_populates="user")  # ← AJOUTER
    # Un utilisateur peut avoir plusieurs tickets associés