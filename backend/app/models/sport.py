# app/models/sport.py
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .ticket import Ticket

class SportBase(SQLModel):
    slug: str = Field(unique=True, index=True)
    nom: str
    image_url: str
    description: str
    lieu: str
    dates_competition: str
    histoire: Optional[str] = None

class Sport(SportBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relations
    epreuves: List["Epreuve"] = Relationship(back_populates="sport")

class EpreuveBase(SQLModel):
    nom_epreuve: str
    date_epreuve: datetime
    heure: str
    places_disponibles: int
    sport_id: int = Field(foreign_key="sport.id")

class Epreuve(EpreuveBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relations
    sport: Optional[Sport] = Relationship(back_populates="epreuves")
    tickets_vendus: List["TicketEpreuve"] = Relationship(back_populates="epreuve")  # Relation many-to-many avec Ticket via TicketEpreuve

class TicketEpreuve(SQLModel, table=True):
    """Table de liaison entre Ticket et Epreuve (many-to-many)"""
    # ⚠️ PAS de champ 'id' pour une table de liaison !
    ticket_id: int = Field(foreign_key="ticket.id", primary_key=True)
    epreuve_id: int = Field(foreign_key="epreuve.id", primary_key=True)
    nombre_places: int = Field(default=1)
    
    # Relations (avec strings pour éviter imports circulaires)
    ticket: Optional["Ticket"] = Relationship(back_populates="epreuves_reservees")
    epreuve: Optional["Epreuve"] = Relationship(back_populates="tickets_vendus")
