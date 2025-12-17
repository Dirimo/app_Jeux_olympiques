from sqlmodel import create_engine, Session
#from app.core.config import settings

# L'URL est definie ici, donc pas besoin du dossier config pour l'instant
DATABASE_URL ="postgresql://olympic_user:secret_password_local_only@localhost:5433/olympic_tickets_db"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session