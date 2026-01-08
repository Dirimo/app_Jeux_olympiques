# backend/app/services/ticket_pdf_service.py
import qrcode
import io
import tempfile
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from datetime import datetime
import json


class TicketPDFService:
    """Service pour générer les PDF des billets avec QR code"""
    
    @staticmethod
    def generate_ticket_pdf(ticket_data: dict) -> bytes:
        """Génère un PDF de billet avec QR code"""
        
        # Créer un PDF en mémoire
        pdf_buffer = io.BytesIO()
        
        # Créer le canvas
        page_width, page_height = letter
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
        
        # ===== HEADER =====
        pdf.setFont("Helvetica-Bold", 28)
        pdf.setFillColor(HexColor("#0052CC"))
        pdf.drawString(0.75*inch, page_height - 0.75*inch, "PARIS 2024")
        
        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(HexColor("#666666"))
        pdf.drawString(6*inch, page_height - 0.75*inch, "Billet Officiel")
        
        # Ligne séparatrice
        pdf.setLineWidth(2)
        pdf.setStrokeColor(HexColor("#0052CC"))
        pdf.line(0.5*inch, page_height - 1.0*inch, 7.5*inch, page_height - 1.0*inch)
        
        # ===== CONTENU PRINCIPAL =====
        y_position = page_height - 1.5*inch
        
        # Titre de l'événement
        pdf.setFont("Helvetica-Bold", 20)
        pdf.setFillColor(HexColor("#1F2937"))
        event_name = ticket_data.get("epreuve_nom", "Evenement Olympique")
        pdf.drawString(0.75*inch, y_position, event_name)
        y_position -= 0.5*inch
        
        # Infos événement
        pdf.setFont("Helvetica", 12)
        pdf.setFillColor(HexColor("#4B5563"))
        
        # Sport
        sport = ticket_data.get("sport_nom", "N/A")
        pdf.drawString(0.75*inch, y_position, f"Sport: {sport}")
        y_position -= 0.3*inch
        
        # Location
        location = ticket_data.get("lieu", "N/A")
        pdf.drawString(0.75*inch, y_position, f"Lieu: {location}")
        y_position -= 0.3*inch
        
        # Date
        date_str = ticket_data.get("date_epreuve", "Date a venir")
        heure_str = ticket_data.get("heure", "")
        date_complete = f"{date_str} {heure_str}".strip()
        pdf.drawString(0.75*inch, y_position, f"Date: {date_complete}")
        y_position -= 0.3*inch
        
        # Nombre de places et offre
        seats = ticket_data.get("nombre_places", 1)
        offer = ticket_data.get("offer_nom", "Standard")
        pdf.drawString(0.75*inch, y_position, f"{seats} place(s) - Offre {offer}")
        y_position -= 0.3*inch
        
        # Prix
        price = ticket_data.get("prix_total", 0)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.setFillColor(HexColor("#059669"))
        pdf.drawString(0.75*inch, y_position, f"Prix: {price} EUR")
        y_position -= 0.7*inch
        
        # ===== QR CODE =====
        qr_data = {
            "clef_achat": ticket_data.get("clef_achat", ""),
            "epreuve": ticket_data.get("epreuve_nom", ""),
            "user": ticket_data.get("user_name", ""),
            "date": ticket_data.get("date_epreuve", ""),
            "places": ticket_data.get("nombre_places", 1)
        }
        
        qr_json = json.dumps(qr_data, ensure_ascii=False)
        
        # Générer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_json)
        qr.make(fit=True)
        
        # Convertir en image PIL
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Sauvegarder le QR code dans un fichier temporaire
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            qr_img.save(tmp_file.name, format='PNG')
            tmp_qr_path = tmp_file.name
        
        # Dessiner le QR code sur le PDF (centré)
        qr_size = 3 * inch
        qr_x = (page_width - qr_size) / 2
        qr_y = y_position - qr_size
        
        pdf.drawImage(tmp_qr_path, qr_x, qr_y, width=qr_size, height=qr_size)
        
        # Supprimer le fichier temporaire
        os.unlink(tmp_qr_path)
        
        y_position = qr_y - 0.5*inch
        
        # ===== INFOS BILLET =====
        pdf.setFont("Helvetica", 9)
        pdf.setFillColor(HexColor("#666666"))
        
        # Clé d'achat
        clef = ticket_data.get("clef_achat", "N/A")
        pdf.drawString(0.75*inch, y_position, f"Cle d'acces: {clef}")
        y_position -= 0.25*inch
        
        # Nom du client
        client_name = ticket_data.get("user_name", "N/A")
        pdf.drawString(0.75*inch, y_position, f"Proprietaire: {client_name}")
        
        # ===== FOOTER =====
        pdf.setLineWidth(1)
        pdf.setStrokeColor(HexColor("#CCCCCC"))
        pdf.line(0.5*inch, 0.7*inch, 7.5*inch, 0.7*inch)
        
        pdf.setFont("Helvetica", 8)
        pdf.setFillColor(HexColor("#999999"))
        pdf.drawString(0.75*inch, 0.4*inch, "Paris 2024 - Billet electronique officiel")
        pdf.drawString(4.5*inch, 0.4*inch, "Presentez ce QR code a l'entree")
        
        # Sauvegarder le PDF
        pdf.save()
        pdf_buffer.seek(0)
        
        return pdf_buffer.getvalue()
