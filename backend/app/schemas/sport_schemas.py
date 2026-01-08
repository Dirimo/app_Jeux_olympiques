# backend/schemas/sport_schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class EpreuveResponse(BaseModel):
    id: int
    nom_epreuve: str
    date_epreuve: datetime
    heure: str
    places_disponibles: int
    
    class Config:
        from_attributes = True


class SportResponse(BaseModel):
    id: int
    slug: str
    nom: str
    image_url: str
    description: str
    lieu: str
    dates_competition: str
    
    class Config:
        from_attributes = True


class SportDetailResponse(SportResponse):
    histoire: Optional[str]
    epreuves: List[EpreuveResponse]
    
    class Config:
        from_attributes = True

