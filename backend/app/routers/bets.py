from datetime import datetime

from app import auth, crud, models, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/bets",
    tags=["Bets"]
)

@router.post("", response_model=schemas.BetResponse, status_code=status.HTTP_201_CREATED)
def place_bet(
    bet: schemas.BetCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    """Place a new bet"""
    try:
        return crud.create_bet(db, current_user.id, bet)
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)
        else:
            raise HTTPException(status_code=400, detail=error_msg)

@router.get("", response_model=list[schemas.BetResponse], status_code=status.HTTP_200_OK)
def get_bets(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    status: str = None,
    bet_type: str = None
):
    return crud.get_user_bets(db, current_user.id, status, bet_type)

@router.get("/{bet_id}", response_model=schemas.BetResponse, status_code=status.HTTP_200_OK)
def get_unique_bet(
    bet_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    bet = crud.get_bet_by_id(db, bet_id)
    
    if not bet:
        raise HTTPException(status_code=404, detail="Bet does not exist")
    
    if current_user.id != bet.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this bet")
    
    return bet