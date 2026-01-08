# backend/schemas/panier_schemas.py
from pydantic import BaseModel


class PanierItemCreate(BaseModel):
    epreuve_id: int
    offer_id: int
    nombre_places: int


class PanierItemResponse(BaseModel):
    id: int
    epreuve_id: int
    offer_id: int
    nombre_places: int
    
    class Config:
        from_attributes = True

