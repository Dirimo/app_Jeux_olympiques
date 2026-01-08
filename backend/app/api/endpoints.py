from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.db.session import get_session
from app.models.offer import Offer

router = APIRouter()

# Cette route répondra sur http://localhost:8000/offers
@router.get("/offers", response_model=List[Offer])
def read_offers(session: Session = Depends(get_session)):
    """
    Récupère la liste de toutes les offres de billets.
    """
    offers = session.exec(select(Offer)).all()
    return offers

