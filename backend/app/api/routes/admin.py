from fastapi import APIRouter
from app.db.session import Session, engine
from app.models.sport import Sport, Epreuve
from app.models.offer import Offer
from sqlmodel import select
from datetime import datetime

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/init-data")
def initialize_data():
    """Initialiser les données de base"""
    
    with Session(engine) as session:
        existing_offers = session.exec(select(Offer)).first()
        if existing_offers:
            return {"status": "warning", "message": "Données déjà présentes"}
        
        # Créer les offres
        offers = [
            Offer(nom_offre="Solo", capacite_personne=1, prix=50.0, description="Billet individuel"),
            Offer(nom_offre="Duo", capacite_personne=2, prix=90.0, description="Billet pour 2"),
            Offer(nom_offre="Famille", capacite_personne=4, prix=150.0, description="Billet famille")
        ]
        for offer in offers:
            session.add(offer)
        session.commit()
        
        # Créer les sports
        sports_data = [
            ("Athlétisme", "athletisme", "Stade de France"),
            ("Natation", "natation", "Paris La Défense Arena"),
        ]
        
        sports_count = 0
        for nom, slug, lieu in sports_data:
            sport = Sport(
                nom=nom, slug=slug,
                description=f"Épreuves de {nom}",
                image_url=f"/images/{slug}.jpg",
                lieu=lieu,
                dates_competition="Juillet-Août 2024",
                histoire="Sport olympique"
            )
            session.add(sport)
            sports_count += 1
        
        session.commit()
        
        return {
            "status": "success",
            "offers_created": 3,
            "sports_created": sports_count
        }

