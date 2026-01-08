# backend/check_db.py
from sqlmodel import Session, select
from app.db.session import engine
from app.models.offer import Offer
from app.models.user import User
from app.models.sport import Sport, Epreuve
from app.models.ticket import Ticket  # ← AJOUTER CETTE LIGNE

with Session(engine) as session:
    # ========== OFFRES ==========
    offres = session.exec(select(Offer)).all()
    print(f"📦 Nombre d'offres : {len(offres)}")
    for o in offres:
        print(f"   - {o.nom_offre}: {o.prix}€ (pour {o.capacite_personne} personne(s))")
    
    # ========== UTILISATEURS ==========
    users = session.exec(select(User)).all()
    print(f"\n👥 Nombre d'utilisateurs : {len(users)}")
    for u in users:
        print(f"   - {u.email} ({u.role})")
    
    # ========== SPORTS (NOUVEAU) ==========
    sports = session.exec(select(Sport)).all()
    print(f"\n🏅 Nombre de sports : {len(sports)}")
    for s in sports:
        print(f"   - {s.nom} ({s.slug}) - {s.lieu}")
    
    # ========== ÉPREUVES (NOUVEAU) ==========
    epreuves = session.exec(select(Epreuve)).all()
    print(f"\n🎯 Nombre d'épreuves : {len(epreuves)}")
    for e in epreuves:
        sport = session.get(Sport, e.sport_id)
        print(f"   - {e.nom_epreuve} ({sport.nom if sport else 'N/A'}) - {e.date_epreuve.strftime('%d/%m/%Y')} à {e.heure}")
        print(f"     Places disponibles: {e.places_disponibles}")
