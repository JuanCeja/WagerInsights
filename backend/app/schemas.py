from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field

# ---------------------- USER SCHEMAS ----------------------

# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    username: str

# Schema for creating a new user (registration)
class UserCreate(UserBase):
    password: str = Field(..., min_length = 8)

# Schema for user response (what API returns)
class UserResponse(UserBase):
    id: int
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True

#Schema for user login
class UserLogin(BaseModel):
    username_or_email: str
    password: str
    
class LeaderBoardEntry(BaseModel):
    username: str
    balance: float
    win_rate: float
    total_bets: int

# ---------------------- TOKEN SCHEMAS ----------------------

# Schema for JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema for token data
class TokenData(BaseModel):
    user_id: Optional[int] = None

# ---------------------- GAME SCHEMAS ----------------------

class GameBase(BaseModel):
    home_team: str
    away_team: str
    home_team_odds: float
    away_team_odds: float
    sport: str
    game_date: datetime
    status: Optional[str] = "upcoming"
    winner: Optional[str] = None
    
class GameCreate(GameBase):
    pass

class GameResponse(GameBase):
    id: int
    settled_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ---------------------- BET SCHEMAS ----------------------

class BetBase(BaseModel):
    game_id: int
    bet_type: Literal["home", "away"]

class BetCreate(BetBase):
    bet_amount: float

class BetResponse(BetCreate):
    id: int
    user_id: int
    status: Optional[str]
    potential_payout: float
    odds_at_bet: float
    created_at: datetime
    settled_at: Optional[datetime]
    updated_at: Optional[datetime]
    game: GameResponse
    
    class Config:
        from_attributes = True


# ---------------------- ADMIN SCHEMAS ----------------------

class GameSettleUpdate(BaseModel):
    winner: Literal["home", "away"]
    
class SettlementSummary(BaseModel):
    settled_game: GameResponse
    bets_settled: list[BetResponse]
    
class BulkSyncRequest(BaseModel):
    sports: list[str]


# ---------------------- ANALYZER SCHEMAS ----------------------

class BetAnalyzeRequest(BaseModel):
    game_id: int
    bet_type: str
    bet_amount: float

class AnalyzerResponse(BaseModel):
    analysis: str


# ---------------------- DEPOSIT SCHEMAS ----------------------

class DepositCreateRequest(BaseModel):
    amount: float = Field(..., gt=0.50)

class DepositCreateResponse(BaseModel):
    payment_intent_id: str
    client_secret: str

class DepositConfirmRequest(BaseModel):
    payment_intent_id: str