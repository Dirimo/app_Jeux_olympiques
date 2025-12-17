from typing import Optional
from sqlmodel import Field, SQLModel

# Modèle offre

class OfferBase(SQLModel):
    nom_offre: str # Solo, Duo, Famille
    description: Optional[str] = None
    prix: float
    capacite_personnee: int # Nombre de personnes pouvant bénéficier de l'offre

class Offer(OfferBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)