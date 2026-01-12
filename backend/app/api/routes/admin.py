from fastapi import APIRouter
from app.db.session import Session, engine
from app.models.sport import Sport, Epreuve
from app.models.offer import Offer
from sqlmodel import select
from datetime import date, time

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/init_data") 
def initialize_data():
    """Initialiser les données de base (offres, sports et épreuves)"""
    
    with Session(engine) as session:
        # Vérifier si des sports existent déjà
        existing_sports = session.exec(select(Sport)).first()
        if existing_sports:
            sports_count = len(session.exec(select(Sport)).all())
            return {
                "status": "warning", 
                "message": "Données déjà présentes",
                "sports_count": sports_count
            }
        
        # 1. Créer les offres
        offers = [
            Offer(nom_offre="Solo", capacite_personne=1, prix=50.0, description="Billet individuel"),
            Offer(nom_offre="Duo", capacite_personne=2, prix=90.0, description="Billet pour 2"),
            Offer(nom_offre="Famille", capacite_personne=4, prix=150.0, description="Billet famille")
        ]
        for offer in offers:
            session.add(offer)
        session.commit()
        
        # 2. Créer les 6 sports avec épreuves
        sports_data = [
            {
                "nom": "Athlétisme",
                "slug": "athletisme",
                "description": "Course, saut, lancer",
                "lieu": "Stade de France",
                "dates_competition": "2-11 Août 2024",
                "histoire": "L'athlétisme est présent aux Jeux Olympiques depuis leur création en 1896.",
                "image_url": "/images/Athletisme.jpg"
            },
            {
                "nom": "Natation",
                "slug": "natation",
                "description": "Nage libre, papillon, dos, brasse",
                "lieu": "Paris La Défense Arena",
                "dates_competition": "27 Juillet - 4 Août 2024",
                "histoire": "Sport olympique depuis 1896, la natation est l'une des disciplines phares des JO.",
                "image_url": "/images/Natation.jpg"
            },
            {
                "nom": "BMX",
                "slug": "bmx",
                "description": "BMX freestyle et racing",
                "lieu": "Saint-Quentin-en-Yvelines",
                "dates_competition": "29 Juillet - 2 Août 2024",
                "histoire": "Le BMX est une discipline olympique depuis 2008.",
                "image_url": "/images/Bmx.jpg"
            },
            {
                "nom": "Boxe",
                "slug": "boxe",
                "description": "Combat, puissance et technique",
                "lieu": "Paris Arena Nord",
                "dates_competition": "27 Juillet - 10 Août 2024",
                "histoire": "La boxe est présente aux JO depuis 1904.",
                "image_url": "/images/Boxe.jpg"
            },
            {
                "nom": "Gymnastique",
                "slug": "gymnastique",
                "description": "Grâce, force et précision artistique",
                "lieu": "Bercy Arena",
                "dates_competition": "27 Juillet - 5 Août 2024",
                "histoire": "La gymnastique artistique est au programme olympique depuis 1896.",
                "image_url": "/images/Gymnastique.jpg"
            },
            {
                "nom": "Escalade",
                "slug": "escalade",
                "description": "Défiez la gravité avec l'escalade sportive",
                "lieu": "Le Bourget",
                "dates_competition": "5-10 Août 2024",
                "histoire": "L'escalade sportive a fait son entrée olympique à Tokyo 2020.",
                "image_url": "/images/Escalade.jpg"
            }
        ]
        
        sports_count = 0
        epreuves_count = 0
        
        for sport_data in sports_data:
            # Créer le sport
            sport = Sport(**sport_data)
            session.add(sport)
            session.commit()
            session.refresh(sport)
            sports_count += 1
            
            # Créer 3 épreuves pour chaque sport
            epreuves = [
                Epreuve(
                    nom_epreuve=f"{sport.nom} - Finale Hommes",
                    sport_id=sport.id,
                    date_epreuve=date(2024, 8, 5),
                    heure=time(20, 0),
                    places_disponibles=5000
                ),
                Epreuve(
                    nom_epreuve=f"{sport.nom} - Finale Femmes",
                    sport_id=sport.id,
                    date_epreuve=date(2024, 8, 6),
                    heure=time(19, 30),
                    places_disponibles=5000
                ),
                Epreuve(
                    nom_epreuve=f"{sport.nom} - Demi-finale",
                    sport_id=sport.id,
                    date_epreuve=date(2024, 8, 4),
                    heure=time(18, 0),
                    places_disponibles=3000
                )
            ]
            
            for epreuve in epreuves:
                session.add(epreuve)
                epreuves_count += 1
            
            session.commit()
        
        return {
            "status": "success",
            "message": "Base de données initialisée avec succès !",
            "offers_created": 3,
            "sports_created": sports_count,
            "epreuves_created": epreuves_count
        }

