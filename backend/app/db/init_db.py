from sqlmodel import Session, select
from app.db.session import engine
from app.models.offer import Offer
from app.models.user import User, UserRole
from app.models.sport import Sport, Epreuve
from app.models.ticket import Ticket  # ← AJOUTER CETTE LIGNE
from app.models.panier import PanierItem
from app.core.security import get_password_hash
import uuid
from datetime import datetime

def init_db():
    with Session(engine) as session:
        
        # ========== 1. OFFRES ==========
        existing_offers = session.exec(select(Offer)).first()
        if not existing_offers:
            print("✅ Création des offres par défaut")
            offres = [
                Offer(nom_offre="Solo", prix=50.0, capacite_personne=1, description="Billet pour 1 personne"),
                Offer(nom_offre="Duo", prix=90.0, capacite_personne=2, description="Billet pour 2 personnes (Couple/Amis)"),
                Offer(nom_offre="Familiale", prix=150.0, capacite_personne=4, description="Offre groupe pour 4 personnes")
            ]
            for o in offres:
                session.add(o)
        else:
            print("ℹ️  Offres déjà existantes")

        # ========== 2. ADMINISTRATEUR ==========
        existing_admin = session.exec(select(User).where(User.email == "admin@olympic.com")).first()
        if not existing_admin:
            print("✅ Création de l'administrateur")
            admin_user = User(
                email="admin@olympic.com",
                nom="Admin",
                prenom="Super",
                role=UserRole.ADMIN,
                hashed_password=get_password_hash("admin123"),
                clef_compte=str(uuid.uuid4())
            )
            session.add(admin_user)
        else:
            print("ℹ️  Administrateur déjà existant")

        # ========== 3. SPORTS (NOUVELLE VÉRIFICATION SÉPARÉE) ==========
        existing_sports = session.exec(select(Sport)).first()
        if not existing_sports:
            print("✅ Création des sports olympiques")
            
            sports_data = [
                {
                    "slug": "athletisme",
                    "nom": "Athlétisme",
                    "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800",
                    "description": "Assistez aux performances exceptionnelles de nos athlètes dans cette discipline olympique.",
                    "lieu": "Stade de France",
                    "dates_competition": "2-11 Août 2024",
                    "histoire": "L'athlétisme est au cœur des Jeux Olympiques depuis l'Antiquité. Ces épreuves symbolisent la quête de l'excellence humaine à travers la course, le saut et le lancer."
                },
                {
                    "slug": "natation",
                    "nom": "Natation",
                    "image_url": "https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=800",
                    "description": "Plongez dans l'action avec les meilleurs nageurs du monde.",
                    "lieu": "Paris La Défense Arena",
                    "dates_competition": "27 Juillet - 4 Août 2024",
                    "histoire": "La natation olympique moderne a débuté en 1896 à Athènes. Depuis, elle n'a cessé d'évoluer avec l'ajout de nouvelles épreuves et techniques."
                },
                {
                    "slug": "bmx",
                    "nom": "BMX",
                    "image_url": "https://images.unsplash.com/photo-1558981852-426c6c22a060?w=800",
                    "description": "Sensations fortes garanties avec le BMX freestyle et racing.",
                    "lieu": "Saint-Quentin-en-Yvelines",
                    "dates_competition": "29 Juillet - 2 Août 2024",
                    "histoire": "Le BMX est entré aux Jeux Olympiques en 2008 à Pékin. Cette discipline combine vitesse, technique et spectacle."
                },
                {
                    "slug": "boxe",
                    "nom": "Boxe",
                    "image_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800",
                    "description": "Combat, puissance et technique au rendez-vous.",
                    "lieu": "Paris Arena Nord",
                    "dates_competition": "27 Juillet - 10 Août 2024",
                    "histoire": "La boxe olympique existe depuis 1904. Elle met en valeur le courage, la stratégie et la maîtrise technique des athlètes."
                },
                {
                    "slug": "gymnastique",
                    "nom": "Gymnastique",
                    "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800",
                    "description": "Grâce, force et précision artistique.",
                    "lieu": "Bercy Arena",
                    "dates_competition": "27 Juillet - 5 Août 2024",
                    "histoire": "La gymnastique artistique est olympique depuis 1896 pour les hommes et 1928 pour les femmes. Elle allie esthétique et prouesses physiques."
                },
                {
                    "slug": "escalade",
                    "nom": "Escalade",
                    "image_url": "https://images.unsplash.com/photo-1522163182402-834f871fd851?w=800",
                    "description": "Défiez la gravité avec l'escalade sportive.",
                    "lieu": "Le Bourget",
                    "dates_competition": "5-10 Août 2024",
                    "histoire": "L'escalade a fait ses débuts olympiques à Tokyo 2020. Elle combine trois disciplines : la vitesse, le bloc et la difficulté."
                }
            ]
            
            sports_crees = []
            for sport_info in sports_data:
                sport = Sport(**sport_info)
                session.add(sport)
                session.flush()
                sports_crees.append(sport)
            
            # ========== 4. ÉPREUVES ==========
            print("✅ Création des épreuves pour chaque sport")
            
            athletisme = next(s for s in sports_crees if s.slug == "athletisme")
            natation = next(s for s in sports_crees if s.slug == "natation")
            bmx = next(s for s in sports_crees if s.slug == "bmx")
            boxe = next(s for s in sports_crees if s.slug == "boxe")
            gymnastique = next(s for s in sports_crees if s.slug == "gymnastique")
            escalade = next(s for s in sports_crees if s.slug == "escalade")
            
            epreuves = [
                # Athlétisme
                Epreuve(sport_id=athletisme.id, nom_epreuve="Finale 100m Hommes", date_epreuve=datetime(2024, 8, 4, 21, 0), heure="21:00", places_disponibles=80000),
                Epreuve(sport_id=athletisme.id, nom_epreuve="Marathon Hommes", date_epreuve=datetime(2024, 8, 10, 8, 0), heure="08:00", places_disponibles=50000),
                Epreuve(sport_id=athletisme.id, nom_epreuve="Saut en hauteur Femmes", date_epreuve=datetime(2024, 8, 7, 19, 0), heure="19:00", places_disponibles=60000),
                
                # Natation
                Epreuve(sport_id=natation.id, nom_epreuve="Finale 100m Nage libre", date_epreuve=datetime(2024, 7, 31, 20, 30), heure="20:30", places_disponibles=15000),
                Epreuve(sport_id=natation.id, nom_epreuve="Relais 4x100m Mixte", date_epreuve=datetime(2024, 7, 27, 19, 0), heure="19:00", places_disponibles=15000),
                Epreuve(sport_id=natation.id, nom_epreuve="200m Papillon Hommes", date_epreuve=datetime(2024, 7, 31, 21, 0), heure="21:00", places_disponibles=15000),
                
                # BMX
                Epreuve(sport_id=bmx.id, nom_epreuve="BMX Racing Finale", date_epreuve=datetime(2024, 8, 2, 15, 0), heure="15:00", places_disponibles=8000),
                Epreuve(sport_id=bmx.id, nom_epreuve="BMX Freestyle Park", date_epreuve=datetime(2024, 7, 31, 14, 0), heure="14:00", places_disponibles=8000),
                
                # Boxe
                Epreuve(sport_id=boxe.id, nom_epreuve="Poids lourds Finale", date_epreuve=datetime(2024, 8, 10, 20, 0), heure="20:00", places_disponibles=12000),
                Epreuve(sport_id=boxe.id, nom_epreuve="Poids moyens Demi-finales", date_epreuve=datetime(2024, 8, 7, 19, 0), heure="19:00", places_disponibles=12000),
                
                # Gymnastique
                Epreuve(sport_id=gymnastique.id, nom_epreuve="Concours général Femmes", date_epreuve=datetime(2024, 8, 1, 18, 0), heure="18:00", places_disponibles=18000),
                Epreuve(sport_id=gymnastique.id, nom_epreuve="Finale Barres asymétriques", date_epreuve=datetime(2024, 8, 4, 16, 0), heure="16:00", places_disponibles=18000),
                
                # Escalade
                Epreuve(sport_id=escalade.id, nom_epreuve="Boulder & Lead Femmes", date_epreuve=datetime(2024, 8, 9, 10, 0), heure="10:00", places_disponibles=5000),
                Epreuve(sport_id=escalade.id, nom_epreuve="Speed Finale Hommes", date_epreuve=datetime(2024, 8, 8, 12, 0), heure="12:00", places_disponibles=5000),
            ]
            
            for epreuve in epreuves:
                session.add(epreuve)
            
            print(f"   - {len(sports_data)} sports créés")
            print(f"   - {len(epreuves)} épreuves créées")
        else:
            print("ℹ️  Sports déjà existants")

        # ========== COMMIT FINAL ==========
        session.commit()
        print("🎉 Initialisation terminée !")

if __name__ == "__main__":
    init_db()
