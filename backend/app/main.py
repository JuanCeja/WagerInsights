import os

from app import crud
from app.database import Base, SessionLocal, engine
from app.routers import admin, bets, games, users
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from fastapi import FastAPI


def auto_settle_all_sports():
    """Background job to automatically settle completed games"""
    

Base.metadata.create_all(bind = engine)

app = FastAPI(title="WagerInsights API", description="Sports betting tracker with virtual money", version = "1.0.0")

app.include_router(users.router)
app.include_router(bets.router)
app.include_router(games.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to WagerInsights API"}

@app.get("/health")
def health_check():
    return {"status": "Healthy"}
