from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

# Modèle ticket de billetterie
class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clef_achat: str # Clé générée lors de l'achat
    qr_code_content: str # Concatenation de la clé d'achat et de l'ID du ticket
    date_achat: datetime = Field(default_factory=datetime.utcnow) # Date et heure de l'achat

    # Clé étrangères
    user_id: int = Field(foreign_key="user.id") # Référence à l'utilisateur
    offer_id: int = Field(foreign_key="offer.id") # Référence à l'offre