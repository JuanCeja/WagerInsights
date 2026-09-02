import os
from datetime import datetime, timezone
from typing import Optional

from app import models, schemas
from app.api_clients.odds_api_client import OddsAPIClient
from app.auth import hash_password
from app.utils.bet_calculator import calculate_payout
from app.utils.odds_parser import parse_api_game_to_model
from app.utils.scores_parser import parse_winner_from_scores
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

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

    return query.order_by(models.Game.game_date).all()

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

def get_game_stats(db: Session) -> dict:
    total = db.query(models.Game).count()
    
    by_sport_query = db.query(
        models.Game.sport,
        func.count(models.Game.id)
    ).group_by(models.Game.sport).all()
    
    by_sport = {sport: count for sport, count in by_sport_query}
    
    by_status_query = db.query(
        models.Game.status,
        func.count(models.Game.id)
    ).group_by(models.Game.status).all()
    
    by_status = {status: count for status, count in by_status_query}
    
    return {
        "total_games": total,
        "by_sport": by_sport,
        "by_status": by_status
    }

# -------------------- Bet CRUD Operations --------------------

def get_bet_by_id(db: Session, bet_id: int):
    return db.query(models.Bet).filter(models.Bet.id == bet_id).first()

def get_user_bets(
    db: Session, 
    user_id: int,
    status: Optional[str] = None,
    bet_type: Optional[str] = None
    ):
    
    query = db.query(models.Bet).options(joinedload(models.Bet.game)).filter(models.Bet.user_id == user_id)
    
    if status is not None:
        query = query.filter(models.Bet.status == status)

    if bet_type is not None:
        query = query.filter(models.Bet.bet_type == bet_type)
    
    return query.order_by(models.Bet.created_at.desc()).all()

def update_bet_status(db: Session, bet_id: int, status: str):
    bet = get_bet_by_id(db, bet_id)
    
    if bet is None:
        return None
    
    if bet.status != "pending":
        return None
    
    bet.status = status
    bet.settled_at = datetime.now(timezone.utc)
    
    if status == "won":
        user = get_user_by_id(db, bet.user_id)
        new_balance = user.balance + bet.potential_payout
        update_user_balance(db, bet.user_id, new_balance)
    
    db.commit()
    db.refresh(bet)
    return bet

def create_bet(db: Session, user_id: int, bet:schemas.BetCreate):

    game = get_game_by_id(db, bet.game_id)
    
    if not game:
        raise ValueError("Game not found")
    
    if game.status != "upcoming":
        raise ValueError("Game is not available for betting")
    
    if bet.bet_type not in ["home", "away"]:
        raise ValueError("Invalid data type")

    user = get_user_by_id(db, user_id)
    
    if bet.bet_amount > user.balance:
        raise ValueError("Insufficient balance")
    
    new_balance = user.balance - bet.bet_amount
    update_user_balance(db, user_id, new_balance)
    
    if bet.bet_type == "home":
        game_odds = game.home_team_odds
    else:
        game_odds = game.away_team_odds
        
    potential_payout = calculate_payout(bet.bet_amount, game_odds)
    
    db_bet = models.Bet(
        user_id = user_id,
        game_id = bet.game_id,
        bet_type = bet.bet_type,
        bet_amount = bet.bet_amount,
        odds_at_bet = game_odds,
        potential_payout = potential_payout,
        status = "pending"
    )
    
    db.add(db_bet)
    db.commit()
    db.refresh(db_bet)
    
    return db_bet


# -------------------- Admin CRUD Operations --------------------

def settle_game(db: Session, game_id: int, winner: str):
    game = get_game_by_id(db, game_id)
    
    if not game:
        raise ValueError("Game not found")
    
    if game.status != "upcoming":
        raise ValueError("Game has already been settled")
    
    if winner not in ["home", "away"]:
        raise ValueError("Winner must be a 'home' or 'away'")
    
    game.status = "completed"
    game.winner = winner
    game.settled_at = datetime.now()
    
    db.commit()
    db.refresh(game)
    
    return game

def settle_bets_for_game(db: Session, game_id: int, winner: str):
    bets = db.query(models.Bet).filter(models.Bet.game_id == game_id, models.Bet.status == "pending").all()
    
    for bet in bets:
        if bet.bet_type == winner:
            bet.status = "won"
            user = get_user_by_id(db, bet.user_id)
            payout = user.balance + bet.potential_payout
            update_user_balance(db, user.id, payout)
        else:
            bet.status = "lost"
    
        bet.settled_at = datetime.now()
        
    db.commit()
    
    return bets





# -------------------- Sync CRUD Operations --------------------

def sync_game_from_api(db: Session, game_data: dict) -> models.Game:
    existing_game = db.query(models.Game).filter(models.Game.external_api_id == game_data["external_api_id"]).first()
    
    if existing_game:
        existing_game.home_team_odds = game_data["home_team_odds"]
        existing_game.away_team_odds = game_data["away_team_odds"]
        existing_game.game_date = game_data["game_date"]
        
        db.commit()
        db.refresh(existing_game)
        return existing_game
    else:
        new_game = models.Game(**game_data)
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        return new_game
    

# -------------------- Auto-Settlement CRUD Operations --------------------

def auto_settle_completed_games(db: Session, sport: str, api_key: str) -> dict:
    """
    Fetch scores for a sport and auto-settle completed games.
    
    Returns summary of games settled.
    """
    settled_games = []
    settled_count = 0
    errors = []
    
    #Fetch scores from API
    client = OddsAPIClient(api_key=api_key)
    try:
        scores_data = client.get_scores(sport)
    except Exception as e:
        return {
            "sport": sport,
            "success": False,
            "error": f"Failed to fetch scores: {str(e)}"
        }
        
    #Process each completed game
    for game in scores_data:
        if not game.get("completed"):
            continue
        
        game_in_db = db.query(models.Game).filter(models.Game.external_api_id == game["id"]).first()
        
        if not game_in_db:
            continue
        
        if game_in_db.status != "completed":
            try:
                winner = parse_winner_from_scores(game)
                settle_game(db, game_in_db.id, winner)
                settle_bets_for_game(db, game_in_db.id, winner)
                settled_count += 1
                settled_games.append(game_in_db.id)
            except Exception as e:
                errors.append(f"Game {game_in_db.id}: {str(e)}")
            


    return {
        "sport": sport,
        "success": True,
        "games_settled": settled_count,
        "errors": errors
    }



# -------------------- Deposit CRUD Operations --------------------


def create_deposit_and_credit_user(db: Session, amount: float, user_id: int, stripe_payment_intent_id: str):
    user = get_user_by_id(db, user_id)
    
    user.balance += amount

    db_deposit = models.Deposit(
        user_id = user.id,
        amount = amount,
        stripe_payment_intent_id = stripe_payment_intent_id,
        status = "succeeded",
    )

    db.add(db_deposit)

    db.commit()
    db.refresh(user)
    db.refresh(db_deposit)

    return user

def get_deposit_by_stripe_id(db: Session, payment_intent_id: str):
    return db.query(models.Deposit).filter(models.Deposit.stripe_payment_intent_id == payment_intent_id).first()