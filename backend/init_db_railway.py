"""
Script d'initialisation de la base de données Railway
"""
from app.db.session import engine, Session
from app.models.sport import Sport, Epreuve
from app.models.offer import Offer
from sqlmodel import select
from datetime import datetime

def init_database():
    """Initialiser la base de données avec les données de base"""
    
    with Session(engine) as session:
        # Vérifier si des données existent déjà
        existing_offers = session.exec(select(Offer)).first()
        if existing_offers:
            print("⚠️ Les données existent déjà, arrêt de l'initialisation")
            return
        
        print("🚀 Initialisation de la base de données...")
        
        # 1. Créer les offres
        offer_solo = Offer(nom_offre="Solo", capacite_personne=1, prix=50.0, description="Billet individuel")
        offer_duo = Offer(nom_offre="Duo", capacite_personne=2, prix=90.0, description="Billet pour 2 personnes")
        offer_famille = Offer(nom_offre="Famille", capacite_personne=4, prix=150.0, description="Billet famille 4 personnes")
        
        session.add(offer_solo)
        session.add(offer_duo)
        session.add(offer_famille)
        session.commit()
        print("✅ Offres créées: Solo, Duo, Famille")
        
        # 2. Créer les sports et épreuves
        sports_data = [
            {
                "nom": "Athlétisme",
                "slug": "athletisme",
                "description": "L'athlétisme regroupe les épreuves de course, saut et lancer",
                "image_url": "/images/athletisme.jpg",
                "lieu": "Stade de France",
                "dates_competition": "26 juillet - 11 août 2024",
                "histoire": "Sport roi des Jeux Olympiques depuis l'Antiquité",
                "epreuves": [
                    {"nom_epreuve": "100m Hommes", "date_epreuve": datetime(2024, 8, 4, 20, 0), "heure": "20:00", "places_disponibles": 80000},
                    {"nom_epreuve": "Marathon Hommes", "date_epreuve": datetime(2024, 8, 10, 8, 0), "heure": "08:00", "places_disponibles": 50000},
                    {"nom_epreuve": "Saut en hauteur Femmes", "date_epreuve": datetime(2024, 8, 6, 19, 0), "heure": "19:00", "places_disponibles": 80000},
                ]
            },
            {
                "nom": "Natation",
                "slug": "natation",
                "description": "Les épreuves de natation se déroulent dans la Paris La Défense Arena",
                "image_url": "/images/natation.jpg",
                "lieu": "Paris La Défense Arena",
                "dates_competition": "27 juillet - 4 août 2024",
                "histoire": "La natation est l'un des sports les plus populaires des JO",
                "epreuves": [
                    {"nom_epreuve": "100m Nage libre Hommes", "date_epreuve": datetime(2024, 7, 31, 20, 30), "heure": "20:30", "places_disponibles": 15000},
                    {"nom_epreuve": "200m Dos Femmes", "date_epreuve": datetime(2024, 8, 1, 19, 0), "heure": "19:00", "places_disponibles": 15000},
                ]
            },
            {
                "nom": "Gymnastique",
                "slug": "gymnastique",
                "description": "Gymnastique artistique et rythmique",
                "image_url": "/images/gymnastique.jpg",
                "lieu": "Bercy Arena",
                "dates_competition": "27 juillet - 5 août 2024",
                "histoire": "La gymnastique fait partie des JO depuis 1896",
                "epreuves": [
                    {"nom_epreuve": "Concours général Hommes", "date_epreuve": datetime(2024, 7, 31, 18, 0), "heure": "18:00", "places_disponibles": 12000},
                    {"nom_epreuve": "Barres asymétriques Femmes", "date_epreuve": datetime(2024, 8, 4, 16, 0), "heure": "16:00", "places_disponibles": 12000},
                ]
            },
        ]
        
        for sport_data in sports_data:
            epreuves_data = sport_data.pop("epreuves")
            sport = Sport(**sport_data)
            session.add(sport)
            session.commit()
            session.refresh(sport)
            
            for epreuve_data in epreuves_data:
                epreuve = Epreuve(**epreuve_data, sport_id=sport.id)
                session.add(epreuve)
            
            session.commit()
            print(f"✅ Sport créé: {sport.nom} avec {len(epreuves_data)} épreuves")
        
        print("\n🎉 Initialisation terminée avec succès !")

if __name__ == "__main__":
    init_database()

