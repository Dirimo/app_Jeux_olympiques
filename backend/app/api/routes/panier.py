from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.panier import PanierItem
from app.models.sport import Sport, Epreuve
from app.models.offer import Offer
import secrets
from datetime import datetime

router = APIRouter(prefix="/api/panier", tags=["Panier"])


@router.get("/user/{user_id}")
def get_panier(user_id: int, session: Session = Depends(get_session)):
    """Récupérer le panier d'un utilisateur avec détails enrichis"""
    statement = select(PanierItem).where(PanierItem.user_id == user_id)
    items = session.exec(statement).all()
    
    result = []
    for item in items:
        epreuve = session.get(Epreuve, item.epreuve_id)
        offer = session.get(Offer, item.offer_id)
        sport = session.get(Sport, epreuve.sport_id) if epreuve else None
        
        # Calculer le prix total
        prix_total = offer.prix * item.nombre_places if offer else 0
        
        result.append({
            "id": item.id,
            "epreuve_id": item.epreuve_id,
            "offer_id": item.offer_id,
            "nombre_places": item.nombre_places,
            "prix_total": prix_total,
            # Infos épreuve
            "epreuve_nom": epreuve.nom_epreuve if epreuve else None,
            "date_epreuve": epreuve.date_epreuve.isoformat() if epreuve else None,
            "heure": epreuve.heure if epreuve else None,
            # Infos sport
            "sport_nom": sport.nom if sport else None,
            # Infos offre
            "offer_nom": offer.nom_offre if offer else None,
        })
    
    return result


@router.post("/user/{user_id}")
def ajouter_au_panier(
    user_id: int,
    epreuve_id: int,
    offer_id: int,
    nombre_places: int = 1,
    session: Session = Depends(get_session)
):
    """Ajouter un article au panier"""
    
    # Vérifier que l'épreuve existe
    epreuve = session.get(Epreuve, epreuve_id)
    if not epreuve:
        raise HTTPException(status_code=404, detail="Épreuve non trouvée")
    
    # Vérifier que l'offre existe
    offer = session.get(Offer, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    
    # Vérifier les places disponibles
    places_necessaires = nombre_places * offer.capacite_personne
    if epreuve.places_disponibles < places_necessaires:
        raise HTTPException(
            status_code=400, 
            detail=f"Seulement {epreuve.places_disponibles} places disponibles"
        )
    
    # Créer l'item du panier
    panier_item = PanierItem(
        user_id=user_id,
        epreuve_id=epreuve_id,
        offer_id=offer_id,
        nombre_places=nombre_places
    )
    
    session.add(panier_item)
    session.commit()
    session.refresh(panier_item)
    
    return {
        "message": "Ajouté au panier avec succès",
        "item_id": panier_item.id,
        "prix_total": offer.prix * nombre_places
    }


@router.delete("/user/{user_id}/item/{item_id}")
def supprimer_du_panier(user_id: int, item_id: int, session: Session = Depends(get_session)):
    """Supprimer un article du panier"""
    statement = select(PanierItem).where(
        PanierItem.id == item_id,
        PanierItem.user_id == user_id
    )
    item = session.exec(statement).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Article non trouvé dans votre panier")
    
    session.delete(item)
    session.commit()
    
    return {"message": "Article supprimé du panier"}


@router.post("/user/{user_id}/valider")
def valider_panier(user_id: int, session: Session = Depends(get_session)):
    """Valider le panier et créer les tickets"""
    from app.models.ticket import Ticket
    from app.models.sport import TicketEpreuve
    
    # Récupérer les items du panier
    statement = select(PanierItem).where(PanierItem.user_id == user_id)
    panier_items = session.exec(statement).all()
    
    if not panier_items:
        raise HTTPException(status_code=400, detail="Votre panier est vide")
    
    tickets_crees = []
    
    for item in panier_items:
        # Vérifier la disponibilité
        epreuve = session.get(Epreuve, item.epreuve_id)
        offer = session.get(Offer, item.offer_id)
        
        if not epreuve:
            raise HTTPException(status_code=404, detail=f"Épreuve {item.epreuve_id} non trouvée")
        
        if not offer:
            raise HTTPException(status_code=404, detail=f"Offre {item.offer_id} non trouvée")
        
        places_necessaires = item.nombre_places * offer.capacite_personne
        
        if epreuve.places_disponibles < places_necessaires:
            raise HTTPException(
                status_code=400, 
                detail=f"Plus assez de places pour {epreuve.nom_epreuve}"
            )
        
        # Calculer le prix total
        prix_total = offer.prix * item.nombre_places
        
        # Générer clé d'achat unique
        clef_achat = secrets.token_urlsafe(16)
        qr_code = f"{clef_achat}-{int(datetime.utcnow().timestamp())}"
        
        # Créer le ticket
        ticket = Ticket(
            user_id=user_id,
            offer_id=offer.id,
            clef_achat=clef_achat,
            qr_code_content=qr_code,
            prix_total=prix_total,
            nombre_places=item.nombre_places  # Ajouter cette info
        )
        
        session.add(ticket)
        session.flush()  # Pour obtenir l'ID du ticket
        
        # Lier le ticket à l'épreuve
        ticket_epreuve = TicketEpreuve(
            ticket_id=ticket.id,
            epreuve_id=epreuve.id,
            nombre_places=item.nombre_places
        )
        session.add(ticket_epreuve)
        
        # Réduire les places disponibles
        epreuve.places_disponibles -= places_necessaires
        
        # Supprimer du panier
        session.delete(item)
        
        tickets_crees.append({
            "ticket_id": ticket.id,
            "epreuve": epreuve.nom_epreuve,
            "prix": prix_total
        })
    
    session.commit()
    
    return {
        "message": f"{len(tickets_crees)} billet(s) acheté(s) avec succès",
        "tickets": tickets_crees
    }
