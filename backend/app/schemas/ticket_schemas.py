# backend/schemas/ticket_schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List


class TicketCreate(BaseModel):
    epreuve_id: int
    offer_id: int
    nombre_places: int


class TicketResponse(BaseModel):
    id: int
    clef_achat: str
    qr_code_content: str
    date_achat: datetime
    prix_total: float
    
    class Config:
        from_attributes = True


class TicketDetailResponse(TicketResponse):
    offer: dict
    epreuves: List[dict]
    
    class Config:
        from_attributes = True

