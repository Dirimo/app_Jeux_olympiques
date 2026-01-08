from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .sport import TicketEpreuve
    from .user import User
    from .offer import Offer

# Modèle ticket de billetterie
class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clef_achat: str  # Clé générée lors de l'achat
    qr_code_content: str  # Concatenation de la clé d'achat et de l'ID du ticket
    date_achat: datetime = Field(default_factory=datetime.utcnow)
    prix_total: float = 0.0  # Prix total payé
    nombre_places: int = Field(default=1)
    
    # Clés étrangères
    user_id: int = Field(foreign_key="user.id")
    offer_id: int = Field(foreign_key="offer.id")
    
    # Relations
    user: Optional["User"] = Relationship(back_populates="tickets")
    offer: Optional["Offer"] = Relationship(back_populates="tickets")
    epreuves_reservees: List["TicketEpreuve"] = Relationship(back_populates="ticket")
