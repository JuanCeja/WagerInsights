from app.database import Base
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    balance = Column(Float, default=1000.0)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    bets = relationship("Bet", back_populates="user")
    deposits = relationship("Deposit", back_populates="user")
    
class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    external_api_id = Column(String, index=True, unique=True, nullable=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_team_odds = Column(Float, nullable=False)
    away_team_odds = Column(Float, nullable=False)
    sport = Column(String, nullable=False)
    game_date = Column(DateTime, nullable=False)
    status = Column(String, default="upcoming")
    winner = Column(String, nullable=True)
    settled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    bets = relationship("Bet", back_populates="game")

class Bet(Base):
    __tablename__ = "bets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    bet_type = Column(String, nullable=False)
    bet_amount = Column(Float, nullable=False)
    odds_at_bet = Column(Float, nullable=False)
    potential_payout = Column(Float, nullable=False)
    status = Column(String, default="pending")
    settled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="bets")
    game = relationship("Game", back_populates="bets")

class Deposit(Base):
    __tablename__ = "deposits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    stripe_payment_intent_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="deposits")