from datetime import datetime
from typing import Optional

from app import crud, models, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

@router.get("", response_model=list[schemas.GameResponse], status_code=status.HTTP_200_OK)
def get_games(
    home_team: Optional[str] = None,
    away_team: Optional[str] = None,
    status: Optional[str] = None,
    sport:Optional[str] = None,
    game_date: Optional[datetime] = None,
    winner: Optional[str] = None,
    settled_at: Optional[datetime] = None,
    created_at: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    games = crud.get_all_games(
        db,
        home_team,
        away_team,
        status,
        sport,
        game_date,
        winner,
        settled_at,
        created_at,
    )
    
    return games