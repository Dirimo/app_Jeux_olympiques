from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.db.session import engine
from app.api.endpoints import router as api_router
from app.api.routes import admin

# Import des modèles EXISTANTS pour créer les tables
from app.models.user import User
from app.models.offer import Offer
from app.models.ticket import Ticket

# Import des NOUVEAUX modèles
from app.models.sport import Sport, Epreuve, TicketEpreuve
from app.models.panier import PanierItem

# Import des routes
from app.api.routes import auth, sports, panier, tickets  # ← Ajouter tickets

# Cette fonction crée les tables au démarrage
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Olympic Ticketing API - Paris 2024")

# Configuration CORS (Cross-Origin Resource Sharing) 
# Indispensable pour que le Frontend (port 3000/5173) puisse appeler le Backend (port 8000)
origins = [
    "http://localhost:5173",  # Port Vite
    "http://localhost:3000",  # Port React (Create React App)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("✅ Base de données initialisée")
    print("📊 Tables créées: User, Offer, Ticket, Sport, Epreuve, TicketEpreuve, PanierItem")

# ========== INCLUSION DES ROUTES ==========

# Routes existantes (offres, etc.)
app.include_router(api_router)

# Nouvelles routes
app.include_router(auth.router)      # /api/auth/register, /api/auth/login
app.include_router(sports.router)    # /api/sports, /api/sports/{slug}
app.include_router(panier.router)    # /api/panier/user/{user_id}
app.include_router(tickets.router)   # /api/tickets/user/{user_id}

@app.get("/")
def read_root():
    return {
        "message": "API Billetterie JO Paris 2024 en ligne 🎉",
        "version": "2.0",
        "documentation": "/docs",
        "endpoints": {
            "offers": "/offers",
            "auth": {
                "register": "/api/auth/register",
                "login": "/api/auth/login"
            },
            "sports": {
                "list": "/api/sports",
                "detail": "/api/sports/{slug}"
            },
            "panier": {
                "get": "/api/panier/user/{user_id}",
                "add": "/api/panier/user/{user_id}",
                "delete": "/api/panier/user/{user_id}/item/{item_id}",
                "validate": "/api/panier/user/{user_id}/valider"
            },
            "tickets": {
                "get_user_tickets": "/api/tickets/user/{user_id}",
                "acheter": "/api/tickets/acheter/{user_id}"
            }
        }
    }
