from datetime import datetime
import os

from app import crud
from app.database import Base, SessionLocal, engine
from app.routers import admin, bets, games, users
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

def auto_settle_all_sports():
    """Background job to automatically settle completed games"""
        
    sports = [
        "basketball_nba",
        "icehockey_nhl",
        "americanfootball_ncaaf",
        "americanfootball_ufl",
        "baseball_mlb",
        "soccer_epl",
        "soccer_mexico_ligamx",
        "soccer_uefa_champs_league",
        "americanfootball_nfl"
    ]
    
    db = SessionLocal()
    api_key = os.getenv("ODDS_API_KEY")
    
    try:
        for sport in sports:
            crud.auto_settle_completed_games(db, sport, api_key)
    finally:
        db.close()
        
def auto_sync_all_sports_and_games():
    """Background job to automatically syncs new sports and games"""
    
    print("\n=== AUTO-SYNC JOB STARTED ===")
    
    sports = [
        "basketball_nba",
        "icehockey_nhl",
        "americanfootball_ncaaf",
        "americanfootball_ufl",
        "baseball_mlb",
        "soccer_mexico_ligamx",
        "soccer_uefa_champs_league"
    ]
    
    db = SessionLocal()
    
    try:
        for sport in sports:
            result = admin._sync_single_sport(sport, db)
            print(f"{sport}: {result.get('created', 0)} created, {result.get('updated', 0)} updated")
    finally:
        db.close()
        print("=== AUTO-SYNC JOB COMPLETE ===\n")

Base.metadata.create_all(bind = engine)

app = FastAPI(title="WagerInsights API", description="Sports betting tracker with virtual money", version = "1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()

scheduler.add_job(
    func=auto_sync_all_sports_and_games,
    trigger="interval",
    hours=12,
    next_run_time=datetime.now()
)
scheduler.add_job(
    func=auto_settle_all_sports,
    trigger="interval",
    hours=1,
    next_run_time=datetime.now()
)

@app.on_event("startup")
def start_scheduler():
    scheduler.start()

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

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
