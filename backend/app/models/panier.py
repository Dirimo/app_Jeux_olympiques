from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime


class PanierItem(SQLModel, table=True):
    """Items temporaires dans le panier avant validation"""
    __tablename__ = "panier_item"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    epreuve_id: int = Field(foreign_key="epreuve.id")
    offer_id: int = Field(foreign_key="offer.id")
    nombre_places: int = 1
    date_ajout: datetime = Field(default_factory=datetime.utcnow)
