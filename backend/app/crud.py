from datetime import datetime, timezone
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

def create_game(db: Session, game: schemas.GameCreate):
    
    created_game = models.Game(**game.model_dump())
    
    db.add(created_game)
    db.commit()
    db.refresh(created_game)

    return created_game

def get_game_by_id(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()

def get_all_games(
    db: Session,
    home_team: Optional[str] = None,
    away_team: Optional[str] = None,
    status: Optional[str] = None,
    sport:Optional[str] = None,
    game_date: Optional[datetime] = None,
    winner: Optional[str] = None,
    settled_at: Optional[datetime] = None,
    created_at: Optional[datetime] = None
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

def update_game_status(db: Session, game_id: int, winner: str, status: str = "completed"):
    game = db.query(models.Game).filter(models.Game.id == game_id).first()
    
    if not game:
        return None
    
    game.status = status
    game.winner = winner
    game.settled_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(game)
    return game


# -------------------- Bet CRUD Operations --------------------

def get_bet_by_id(db: Session, id: int):
    return db.query(models.Bet).filter(models.Bet.id == id).first()

def get_user_bets(
    db: Session,
    id: Optional[int] = None,
    status: Optional[str] = None,
    bet_type: Optional[str] = None,
    bet_amount: Optional[str] = None,
    created_at: Optional[datetime] = None
    ):
    
    query = db.query(models.Bet)
    
    if id is not None:
        query = query.filter(models.Bet.id == id)
        
    if status is not None:
        query = query.filter(models.Bet.status == status)
        
    if bet_type is not None:
        query = query.filter(models.Bet.bet_type == bet_type)
        
    if bet_amount is not None:
        query = query.filter(models.Bet.bet_amount == bet_amount)
        
    if created_at is not None:
        query = query.filter(models.Bet.created_at == created_at)
        
    return query.all()

def update_bet_status(db: Session, id: int, status: str):
    bet = db.query.filter(models.Bet.id == id).first()
    
    if bet is None:
        return None
    
    bet.status = status
    bet.settled_at = datetime.now(timezone.utc)
    
    db.commit()
    db.refresh(bet)
    return bet

def create_bet(db: Session, game_id: int, bet_type: str, bet_amount: float, user_id: int):
    # first check if game is pending
    
    # then grab how much funds user has
    
    # if bet amount is < funds proceed else return an error
    
    # subtract amount betted from users funds
    
    # submit bet
    
    # return bet