# app/api/routes/sports.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.sport import Sport, Epreuve

router = APIRouter(prefix="/api/sports", tags=["Sports"])


@router.get("")
def get_all_sports(session: Session = Depends(get_session)):
    statement = select(Sport)
    sports = session.exec(statement).all()
    return sports


@router.get("/{slug}")
def get_sport_detail(slug: str, session: Session = Depends(get_session)):
    statement = select(Sport).where(Sport.slug == slug)
    sport = session.exec(statement).first()
    
    if not sport:
        raise HTTPException(status_code=404, detail="Sport non trouvé")
    
    # Charger les épreuves
    epreuves_statement = select(Epreuve).where(Epreuve.sport_id == sport.id)
    epreuves = session.exec(epreuves_statement).all()
    
    return {
        **sport.dict(),
        "epreuves": [e.dict() for e in epreuves]
    }
