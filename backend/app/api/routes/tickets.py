from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.responses import StreamingResponse
from app.services.ticket_pdf_service import TicketPDFService    
from typing import List
from app.db.session import get_session
from app.models.ticket import Ticket
from app.models.offer import Offer
from app.models.sport import Epreuve, Sport, TicketEpreuve
from app.models.panier import PanierItem
from app.models.user import User
import secrets
import io
from datetime import datetime


router = APIRouter(prefix="/api/tickets", tags=["Tickets"])


@router.get("/user/{user_id}")
def get_user_tickets(user_id: int, session: Session = Depends(get_session)):
    """Récupérer tous les billets achetés d'un utilisateur avec détails enrichis"""
    try:
        print(f"📋 Récupération des tickets pour user_id: {user_id}")
        
        statement = select(Ticket).where(Ticket.user_id == user_id)
        tickets = session.exec(statement).all()
        
        print(f"✅ {len(tickets)} tickets trouvés")
        
        if not tickets:
            return []
        
        result = []
        for ticket in tickets:
            print(f"🎫 Traitement ticket {ticket.id}")
            
            # Récupérer l'offre
            offer = session.get(Offer, ticket.offer_id)
            if not offer:
                print(f"⚠️ Offre {ticket.offer_id} non trouvée pour ticket {ticket.id}")
                continue
            
            # Récupérer les épreuves liées via TicketEpreuve
            statement_te = select(TicketEpreuve).where(TicketEpreuve.ticket_id == ticket.id)
            ticket_epreuves = session.exec(statement_te).all()
            
            if not ticket_epreuves:
                print(f"⚠️ Aucune épreuve liée au ticket {ticket.id}")
                continue
            
            for te in ticket_epreuves:
                epreuve = session.get(Epreuve, te.epreuve_id)
                if not epreuve:
                    print(f"⚠️ Épreuve {te.epreuve_id} non trouvée")
                    continue
                
                sport = session.get(Sport, epreuve.sport_id) if epreuve else None
                
                # Adapter les noms de champs pour le frontend
                ticket_data = {
                    "id": ticket.id,
                    "epreuve_id": epreuve.id,
                    "epreuve_nom": epreuve.nom_epreuve if hasattr(epreuve, 'nom_epreuve') else epreuve.nom,
                    "sport_nom": sport.nom if sport else None,
                    "date": epreuve.date_epreuve.isoformat() if hasattr(epreuve, 'date_epreuve') and epreuve.date_epreuve else (epreuve.date.isoformat() if hasattr(epreuve, 'date') and epreuve.date else None),
                    "heure": epreuve.heure if hasattr(epreuve, 'heure') else None,
                    "lieu": sport.lieu if sport and hasattr(sport, 'lieu') else None,
                    "offer_id": offer.id,
                    "offer_nom": offer.nom_offre if hasattr(offer, 'nom_offre') else offer.nom,
                    "prix_unitaire": float(offer.prix),
                    "nombre_places": ticket.nombre_places if hasattr(ticket, 'nombre_places') else 1,
                    "prix_total": float(ticket.prix_total),
                    "statut": "validé",
                    "date_achat": ticket.date_achat.isoformat() if ticket.date_achat else None,
                    "clef_achat": ticket.clef_achat if hasattr(ticket, 'clef_achat') else None,
                    "qr_code": ticket.qr_code_content if hasattr(ticket, 'qr_code_content') else None,
                }
                
                print(f"✅ Ticket formaté: {ticket_data}")
                result.append(ticket_data)
        
        print(f"✅ Retour de {len(result)} tickets")
        return result
        
    except Exception as e:
        print(f"❌ ERREUR lors de la récupération des tickets: {type(e).__name__}")
        print(f"❌ Message: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.post("/acheter/{user_id}")
def acheter_ticket_depuis_panier(user_id: int, session: Session = Depends(get_session)):
    """Valider le panier et créer les tickets (alternative à /panier/valider)"""
    try:
        print(f"🛒 Validation panier pour user_id: {user_id}")
        
        # Récupérer les items du panier
        statement = select(PanierItem).where(PanierItem.user_id == user_id)
        panier_items = session.exec(statement).all()
        
        if not panier_items:
            raise HTTPException(status_code=400, detail="Votre panier est vide")
        
        print(f"📦 {len(panier_items)} items dans le panier")
        
        tickets_crees = []
        
        for item in panier_items:
            print(f"🎫 Traitement item panier: epreuve_id={item.epreuve_id}, offer_id={item.offer_id}")
            
            # Vérifier l'épreuve
            epreuve = session.get(Epreuve, item.epreuve_id)
            if not epreuve:
                raise HTTPException(status_code=404, detail=f"Épreuve {item.epreuve_id} non trouvée")
            
            # Vérifier l'offre
            offer = session.get(Offer, item.offer_id)
            if not offer:
                raise HTTPException(status_code=404, detail="Offre non trouvée")
            
            # Calculer les places nécessaires
            capacite = offer.capacite_personne if hasattr(offer, 'capacite_personne') else 1
            places_necessaires = item.nombre_places * capacite
            
            # Vérifier la disponibilité
            places_dispo = epreuve.places_disponibles if hasattr(epreuve, 'places_disponibles') else 1000
            if places_dispo < places_necessaires:
                raise HTTPException(
                    status_code=400,
                    detail=f"Plus assez de places (disponibles: {places_dispo}, demandées: {places_necessaires})"
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
                nombre_places=item.nombre_places
            )
            
            session.add(ticket)
            session.flush()  # Pour obtenir l'ID du ticket
            
            print(f"✅ Ticket créé: id={ticket.id}")
            
            # Lier le ticket à l'épreuve
            ticket_epreuve = TicketEpreuve(
                ticket_id=ticket.id,
                epreuve_id=epreuve.id,
                nombre_places=item.nombre_places
            )
            session.add(ticket_epreuve)
            
            # Réduire les places disponibles
            if hasattr(epreuve, 'places_disponibles'):
                epreuve.places_disponibles -= places_necessaires
            
            # Supprimer l'item du panier
            session.delete(item)
            
            nom_epreuve = epreuve.nom_epreuve if hasattr(epreuve, 'nom_epreuve') else epreuve.nom
            
            tickets_crees.append({
                "ticket_id": ticket.id,
                "epreuve": nom_epreuve,
                "prix": prix_total
            })
        
        session.commit()
        
        print(f"✅ {len(tickets_crees)} tickets créés avec succès")
        
        return {
            "message": f"{len(tickets_crees)} billet(s) acheté(s) avec succès",
            "tickets": tickets_crees
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de l'achat: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")


@router.get("/{ticket_id}/download-pdf")
async def download_ticket_pdf(
    ticket_id: int,
    session: Session = Depends(get_session)
):
    """Télécharger le billet en PDF avec QR code"""
    try:
        print(f"📥 Génération du PDF pour le ticket {ticket_id}")
        
        # Récupérer le ticket
        ticket = session.get(Ticket, ticket_id)
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Billet non trouvé")
        
        # Récupérer l'utilisateur
        user = session.get(User, ticket.user_id)
        user_name = f"{user.prenom} {user.nom}" if user else "Client"
        
        # Récupérer l'offre
        offer = session.get(Offer, ticket.offer_id)
        
        if not offer:
            raise HTTPException(status_code=404, detail="Offre non trouvée")
        
        # Récupérer l'épreuve liée
        statement_te = select(TicketEpreuve).where(TicketEpreuve.ticket_id == ticket.id)
        ticket_epreuve = session.exec(statement_te).first()
        
        epreuve = None
        sport = None
        
        if ticket_epreuve:
            epreuve = session.get(Epreuve, ticket_epreuve.epreuve_id)
            if epreuve:
                sport = session.get(Sport, epreuve.sport_id)
        
        # Préparer les données pour le PDF
        ticket_data = {
            "clef_achat": ticket.clef_achat,
            "epreuve_nom": epreuve.nom_epreuve if epreuve else "Événement Paris 2024",
            "sport_nom": sport.nom if sport else "Sport",
            "lieu": sport.lieu if sport else "Paris",
            "date_epreuve": epreuve.date_epreuve.strftime("%d/%m/%Y") if epreuve and epreuve.date_epreuve else "Date à confirmer",
            "heure": epreuve.heure if epreuve else "",
            "offer_nom": offer.nom_offre if hasattr(offer, 'nom_offre') else "Offre",
            "prix_total": float(ticket.prix_total),
            "nombre_places": ticket.nombre_places if hasattr(ticket, 'nombre_places') else 1,
            "user_name": user_name
        }
        
        # Générer le PDF
        pdf_bytes = TicketPDFService.generate_ticket_pdf(ticket_data)
        
        print(f"✅ PDF généré avec succès pour le ticket {ticket_id}")
        
        # Retourner le PDF
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=billet_paris2024_{ticket.clef_achat}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur lors de la génération du PDF: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du PDF: {str(e)}")
