from datetime import datetime

from app import crud, models, schemas, auth
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/bets",
    tags=["Bets"]
)

@router.post("/place_bet", response_model=schemas.BetResponse, status_code=status.HTTP_201_CREATED)
def place_bet(
    bet: schemas.BetCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = (get_db)
):
    