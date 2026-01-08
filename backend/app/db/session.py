import os
from sqlmodel import create_engine, Session

# Récupérer l'URL de la base de données depuis les variables d'environnement
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://olympic_user:secret_password_local_only@localhost:5433/olympic_tickets_db")

# Railway utilise postgres:// mais SQLAlchemy nécessite postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
