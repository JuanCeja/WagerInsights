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

# get all games with optional filter
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

@router.get("/game_stats", status_code=status.HTTP_200_OK)
def get_game_statistics(db: Session = Depends(get_db)):
    game_stat_details = crud.get_game_stats(db)
    return game_stat_details

# get game single game by id
@router.get("/{game_id}", response_model=schemas.GameResponse, status_code=status.HTTP_200_OK)
def get_specific_game(game_id: int, db: Session = Depends(get_db)):
    game = crud.get_game_by_id(db, game_id)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game does not exist"
        )
        
    return game