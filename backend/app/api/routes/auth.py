from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.user import User, UserRole
from app.core.security import verify_password
import bcrypt
import secrets

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class UserCreate:
    def __init__(self, email: str, nom: str, prenom: str, password: str):
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.password = password

class UserLogin:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

@router.post("/register")
def register(email: str, nom: str, prenom: str, password: str, session: Session = Depends(get_session)):
    """Inscription d'un nouvel utilisateur"""
    # Vérifier si l'email existe
    statement = select(User).where(User.email == email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    
    # Hasher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Générer une clé de compte unique
    clef_compte = secrets.token_urlsafe(32)
    
    # Créer l'utilisateur
    new_user = User(
        email=email,
        nom=nom,
        prenom=prenom,
        hashed_password=hashed_password.decode('utf-8'),
        clef_compte=clef_compte,
        role=UserRole.CLIENT
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {
        "id": new_user.id,  # ← Déjà correct
        "email": new_user.email,
        "nom": new_user.nom,
        "prenom": new_user.prenom,
        "role": new_user.role,
        "message": "Compte créé avec succès"
    }

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    """Connexion d'un utilisateur"""
    # Chercher l'utilisateur
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    # Vérifier le mot de passe
    if not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Compte désactivé")
    
    # Sauvegarder l'utilisateur dans la session
    return {
        "id": user.id,
        "email": user.email,
        "nom": user.nom,
        "prenom": user.prenom,
        "role": user.role,
        "message": "Connexion réussie"
    }
