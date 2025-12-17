from fastapi import FastAPI
from sqlmodel import SQLModel
from app.db.session import engine
from app.models.user import User
from app.models.offer import Offer
from app.models.ticket import Ticket

# Cette fonction crée les tables au démarrage
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Olympic Ticketing API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "API Billetterie JO 2024 en ligne"}
