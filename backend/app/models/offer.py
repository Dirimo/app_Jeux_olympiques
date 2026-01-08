from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .ticket import Ticket

# Modèle offre

class OfferBase(SQLModel):
    nom_offre: str  # Solo, Duo, Famille
    description: Optional[str] = None
    prix: float
    capacite_personne: int  # Nombre de personnes pouvant bénéficier de l'offre

class Offer(OfferBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relations
    tickets: List["Ticket"] = Relationship(back_populates="offer") # Une offre peut avoir plusieurs tickets associés
