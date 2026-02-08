from datetime import datetime

from app import auth, crud, models, schemas
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/{game_id}", status_code=status.HTTP_200_OK)
def settle_game_and_bets(game_update: schemas.GameSettleUpdate, game_id:int, db: Session = Depends(get_db)):
    crud.settle_game(db, game_id, game_update.winner)
    crud.settle_bets_for_game(db, game_id, game_update.winner)