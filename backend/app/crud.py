from datetime import datetime

from app import models, schemas
from app.auth import hash_password
from sqlalchemy.orm import Session

# -------------------- User CRUD Operations --------------------

def get_user_by_email(db: Session, email: str):
    """Get a user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, id: int):
    """Get a user by ID"""
    return db.query(models.User).filter(models.User.id == id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user"""
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        email = user.email,
        username = user.username,
        hashed_password = hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_balance(db: Session, user_id: int, new_balance: float):
    """Update a user's balance"""
    user = get_user_by_id(db, user_id)
    if user:
        user.balance = new_balance
        db.commit()
        db.refresh(user)
    return user

# -------------------- Game CRUD Operations --------------------

def create_game(
    home_team: str,
    away_team: str, 
    home_team_odds: float,
    away_team_odds: float,
    sport: str,
    game_date: datetime,
    status: str,
    winner: str,
    db: Session ):
    
    # ********* here in the parameters i think i need to add the Game Create Schema and maybe not all the field parametes. fix this then proceed to get all games function
    
    created_game = {
        home_team: home_team,
        away_team: away_team, 
        home_team_odds: home_team_odds,
        away_team_odds: away_team_odds,
        sport: sport,
        game_date: game_date,
        status: status,
        winner: winner,
    }
    
    db.add(created_game)
    db.commit()
    db.refresh(created_game)

    return created_game

def get_game_by_id(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def get_all_games(db. Session, )
# -------------------- Bet CRUD Operations --------------------