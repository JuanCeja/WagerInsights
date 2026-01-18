from datetime import datetime
from typing import Optional

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

def create_game(game: schemas.GameCreate, db: Session):
    
    created_game = models.Game(**game.model_dump())
    
    db.add(created_game)
    db.commit()
    db.refresh(created_game)

    return created_game

def get_game_by_id(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def get_all_games(
    home_team: Optional[str],
    away_team: Optional[str],
    status: Optional[str],
    sport:Optional[str],
    game_date: Optional[datetime],
    winner: Optional[str],
    settled_at: Optional[datetime],
    created_at: Optional[datetime],
    db: Session
    ):
    
    query = db.query(models.Game)
    
    if home_team is not None:
        query = query.filter(models.Game.home_team == home_team)
    
    if away_team is not None:
        query = query.filter(models.Game.away_team == away_team)
    
    if status is not None:
        query = query.filter(models.Game.status == status)
    
    if sport is not None:
        query = query.filter(models.Game.sport == sport)
    
    if game_date is not None:
        query = query.filter(models.Game.game_date == game_date)
    
    if winner is not None:
        query = query.filter(models.Game.winner == winner)
    
    if settled_at is not None:
        query = query.filter(models.Game.settled_at == settled_at)
    
    if created_at is not None:
        query = query.filter(models.Game.created_at == created_at)
        
    return query.all()

# -------------------- Bet CRUD Operations --------------------